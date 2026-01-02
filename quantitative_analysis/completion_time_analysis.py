"""
Mann-Whitney U Test for Survey Completion Time Analysis.

This module performs non-parametric Mann-Whitney U tests to compare
completion times between different survey formats (single page vs. slides).

The analysis is conducted for:
1. Overall sample
2. Respondents with text responses
3. Respondents without text responses
"""

import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu


# Constants
MAX_INTERVIEW_TIME = 3600  # Maximum time in seconds (1 hour)
MIN_RESPONSES = 5  # Minimum number of responses required


def filter_data(matrix):
    """Apply filtering criteria.
    
    Args:
        matrix: DataFrame with survey data
        
    Returns:
        Filtered DataFrame
    """
    
    # Apply filters
    matrix_filtered = matrix[
        (matrix['interviewtime'] < MAX_INTERVIEW_TIME) &
        (matrix['BrOdgovora'] >= MIN_RESPONSES)
    ].copy()
    
    print(f"Filtered data shape: {matrix_filtered.shape}")
    print(f"Rows removed: {len(matrix) - len(matrix_filtered)}")
    print(f"\nFiltering criteria:")
    print(f"  - Interview time < {MAX_INTERVIEW_TIME} seconds ({MAX_INTERVIEW_TIME/60:.0f} minutes)")
    print(f"  - Number of responses >= {MIN_RESPONSES}")
    
    return matrix_filtered


def get_descriptive_stats(data, label):
    """Calculate descriptive statistics for interview time.
    
    Args:
        data: Series containing interview time values
        label: Label for the data group
        
    Returns:
        Dictionary with descriptive statistics
    """
    if len(data) == 0:
        return None
    
    return {
        'label': label,
        'n': len(data),
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data, ddof=1),
        'min': np.min(data),
        'max': np.max(data),
        'q25': np.percentile(data, 25),
        'q75': np.percentile(data, 75)
    }


def print_descriptive_stats(stats):
    """Print formatted descriptive statistics.
    
    Args:
        stats: Dictionary with descriptive statistics
    """
    if stats is None:
        print("  No data available")
        return
    
    print(f"  Sample size: {stats['n']}")
    print(f"  Mean: {stats['mean']:.2f} seconds ({stats['mean']/60:.2f} minutes)")
    print(f"  Median: {stats['median']:.2f} seconds ({stats['median']/60:.2f} minutes)")
    print(f"  Std Dev: {stats['std']:.2f} seconds")
    print(f"  Range: {stats['min']:.2f} - {stats['max']:.2f} seconds")
    print(f"  IQR: {stats['q25']:.2f} - {stats['q75']:.2f} seconds")


def perform_mann_whitney_test(group1, group2, group1_name, group2_name, 
                               test_description, alpha=0.05):
    """Perform Mann-Whitney U test and display results.
    
    Args:
        group1: First group data (Series)
        group2: Second group data (Series)
        group1_name: Name of first group
        group2_name: Name of second group
        test_description: Description of the comparison
        alpha: Significance level (default 0.05)
        
    Returns:
        Dictionary with test results
    """
    print("\n" + "="*70)
    print(f"Mann-Whitney U Test: {test_description}")
    print("="*70)
    
    # Validate data
    if len(group1) == 0 or len(group2) == 0:
        print("\nError: One or both groups are empty. Cannot perform test.")
        return None
    
    # Descriptive statistics
    print(f"\n{group1_name}:")
    stats1 = get_descriptive_stats(group1, group1_name)
    print_descriptive_stats(stats1)
    
    print(f"\n{group2_name}:")
    stats2 = get_descriptive_stats(group2, group2_name)
    print_descriptive_stats(stats2)
    
    # Perform Mann-Whitney U test
    try:
        u_statistic, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
        
        print(f"\nTest Results:")
        print(f"  U-statistic: {u_statistic:.2f}")
        print(f"  p-value: {p_value:.4f}")
        
        # Interpretation
        if p_value < alpha:
            print(f"\n  ✓ Result: Statistically significant (p < {alpha})")
            print(f"  There is a significant difference in completion time between")
            print(f"  {group1_name} and {group2_name}.")
            
            # Indicate direction
            if stats1['median'] < stats2['median']:
                print(f"  {group1_name} has shorter completion times.")
            else:
                print(f"  {group2_name} has shorter completion times.")
        else:
            print(f"\n  ✗ Result: Not statistically significant (p >= {alpha})")
            print(f"  No significant difference in completion time between groups.")
        
        return {
            'description': test_description,
            'group1': group1_name,
            'group2': group2_name,
            'n1': len(group1),
            'n2': len(group2),
            'median1': stats1['median'],
            'median2': stats2['median'],
            'u_statistic': u_statistic,
            'p_value': p_value,
            'significant': p_value < alpha
        }
    
    except Exception as e:
        print(f"\nError performing Mann-Whitney U test: {e}")
        return None


def analyze_by_format(matrix, description="Overall Sample"):
    """Compare completion times between Format 1 and Format 2.
    
    Args:
        matrix: DataFrame with survey data
        description: Description of the subset being analyzed
        
    Returns:
        Dictionary with test results
    """
    format1 = matrix[matrix['FormatUpitnika'] == 1]['interviewtime']
    format2 = matrix[matrix['FormatUpitnika'] == 2]['interviewtime']
    
    return perform_mann_whitney_test(
        format1, format2,
        "Format 1 (Single Page)",
        "Format 2 (Slides)",
        description
    )


def print_summary_table(all_results):
    """Print summary table of all Mann-Whitney U tests.
    
    Args:
        all_results: List of result dictionaries
    """
    print("\n" + "="*70)
    print("SUMMARY TABLE: Mann-Whitney U Tests")
    print("="*70)
    
    print(f"\n{'Analysis':<25} {'n1':<8} {'n2':<8} {'U-stat':<12} "
          f"{'p-value':<12} {'Significant'}")
    print("-"*70)
    
    for result in all_results:
        if result is None:
            continue
        
        sig_marker = "Yes**" if result['significant'] else "No"
        desc_short = result['description'][:23]
        
        print(f"{desc_short:<25} {result['n1']:<8} {result['n2']:<8} "
              f"{result['u_statistic']:<12.2f} {result['p_value']:<12.4f} {sig_marker}")
    
    print("\n** Statistically significant at α = 0.05")
    
    # Median comparison
    print("\n" + "="*70)
    print("Median Completion Times (seconds)")
    print("="*70)
    print(f"\n{'Analysis':<25} {'Format 1':<15} {'Format 2':<15} {'Difference'}")
    print("-"*70)
    
    for result in all_results:
        if result is None:
            continue
        
        diff = result['median1'] - result['median2']
        desc_short = result['description'][:23]
        
        print(f"{desc_short:<25} {result['median1']:>13.1f}s "
              f"{result['median2']:>13.1f}s {diff:>+13.1f}s")


def main():
    print("="*70)
    print("Mann-Whitney U Test: Survey Completion Time Analysis")
    print("="*70)
    print("\nHypothesis: Survey format affects completion time")
    print("Comparing Format 1 (Single Page) vs. Format 2 (Slides)")

    # Load data
    print("\nLoading data from 'data/input/matrix-recoded.csv'...")
    matrix = pd.read_csv("data/input/matrix-recoded.csv")
    print(f"Data loaded: {len(matrix)} records")
    
    # Filter data
    matrix = filter_data(matrix)
    
    # Store results
    all_results = []
    
    # Test 1: Overall comparison
    result1 = analyze_by_format(matrix, "Overall Sample")
    all_results.append(result1)
    
    # Test 2: Respondents WITH text responses
    has_response = matrix[matrix['O123Ima1Nema2'] == 1].copy()
    print(f"\n\nSubset: Respondents with text responses (n = {len(has_response)})")
    
    if len(has_response) > 0:
        result2 = analyze_by_format(has_response, "With Text Responses")
        all_results.append(result2)
    else:
        print("No respondents with text responses found.")
        all_results.append(None)
    
    # Test 3: Respondents WITHOUT text responses
    no_response = matrix[matrix['O123Ima1Nema2'] == 2].copy()
    print(f"\n\nSubset: Respondents without text responses (n = {len(no_response)})")
    
    if len(no_response) > 0:
        result3 = analyze_by_format(no_response, "Without Text Responses")
        all_results.append(result3)
    else:
        print("No respondents without text responses found.")
        all_results.append(None)
    
    # Print summary
    print_summary_table(all_results)
    
    # Overall conclusion
    print("\n" + "="*70)
    print("OVERALL CONCLUSION")
    print("="*70)
    
    significant_count = sum(1 for r in all_results if r and r['significant'])
    total_tests = sum(1 for r in all_results if r is not None)
    
    print(f"\nSignificant results: {significant_count} out of {total_tests} tests")
    
    if significant_count > 0:
        print("\nThe survey format appears to have an effect on completion time.")
        print("Review the specific comparisons above for details.")
    else:
        print("\nNo significant differences in completion time were found between")
        print("Format 1 (Single Page) and Format 2 (Slides) across all comparisons.")
    
    print("\n" + "="*70)
    print("Analysis Complete!")
    print("="*70)


if __name__ == "__main__":
    main()
