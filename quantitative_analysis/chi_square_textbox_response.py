"""
Chi-square test analysis with effect size (Phi coefficient).

H2: Larger text boxes for open-ended questions will be associated
with fewer non-responses.

This module performs chi-square tests and calculates the Phi coefficient
to measure the effect size of the relationship between text box size
and response rates.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats

def calculate_phi(chi2_value, total_n):
    """Calculate Phi coefficient as a measure of effect size.
    
    The Phi coefficient measures the strength of association between
    two binary variables. It ranges from 0 to 1, where:
    - 0.1 = small effect
    - 0.3 = medium effect
    - 0.5 = large effect
    
    Args:
        chi2_value: Chi-square test statistic
        total_n: Total sample size
        
    Returns:
        Phi coefficient value
    """
    return np.sqrt(chi2_value / total_n)


def interpret_phi(phi_value):
    """Interpret the Phi coefficient effect size.
    
    Args:
        phi_value: The calculated Phi coefficient
        
    Returns:
        String describing the effect size
    """
    if phi_value < 0.1:
        return "negligible"
    elif phi_value < 0.3:
        return "small"
    elif phi_value < 0.5:
        return "medium"
    else:
        return "large"


def perform_chi_square_with_phi(large_box, small_box, question_name):
    """Perform chi-square test and calculate Phi coefficient.
    
    Args:
        large_box: List of [responses, non_responses] for large text box
        small_box: List of [responses, non_responses] for small text box
        question_name: Name/description of the question being analyzed
        
    Returns:
        Dictionary containing test results including Phi coefficient
    """
    chi2, p_value, dof, expected = stats.chi2_contingency([large_box, small_box])
    total_n = sum(large_box) + sum(small_box)
    phi = calculate_phi(chi2, total_n)
    
    return {
        'question': question_name,
        'chi2': chi2,
        'p_value': p_value,
        'dof': dof,
        'expected': expected,
        'phi': phi,
        'effect_size': interpret_phi(phi),
        'total_n': total_n,
        'large_box': large_box,
        'small_box': small_box
    }


def print_test_results(results, alpha=0.05):
    """Print formatted chi-square test results with Phi coefficient.
    
    Args:
        results: Dictionary containing test results
        alpha: Significance level (default 0.05)
    """
    print("\n" + "="*70)
    print(f"Chi-Square Test: {results['question']}")
    print("="*70)
    
    print(f"\nLarge text box: {results['large_box'][0]} responses, "
          f"{results['large_box'][1]} non-responses")
    print(f"Small text box: {results['small_box'][0]} responses, "
          f"{results['small_box'][1]} non-responses")
    print(f"Total sample size: {results['total_n']}")
    
    print(f"\nChi-square statistic: {results['chi2']:.4f}")
    print(f"p-value: {results['p_value']:.4f}")
    print(f"Phi coefficient: {results['phi']:.4f}")
    print(f"Effect size: {results['effect_size']}")
    
    if results['p_value'] < alpha:
        print(f"\n✓ Result: Statistically significant (p < {alpha})")
        print(f"  The relationship between text box size and response rate is")
        print(f"  significant with a {results['effect_size']} effect size.")
    else:
        print(f"\n✗ Result: Not statistically significant (p >= {alpha})")
        print("  Insufficient evidence to support the hypothesis.")


def calculate_response_rate(responses, non_responses):
    """Calculate response rate percentage.
    
    Args:
        responses: Number of responses
        non_responses: Number of non-responses
        
    Returns:
        Response rate as percentage
    """
    total = responses + non_responses
    if total == 0:
        return 0.0
    return (responses / total) * 100


def print_summary_table(all_results):
    """Print comprehensive summary table with Phi coefficients.
    
    Args:
        all_results: List of result dictionaries
    """
    print("\n" + "="*80)
    print("SUMMARY TABLE: Chi-Square Tests with Effect Sizes")
    print("="*80)
    print(f"\n{'Question':<35} {'Chi²':<10} {'p-value':<10} "
          f"{'Phi':<10} {'Effect':<15}")
    print("-"*80)
    
    for result in all_results:
        significant = "Yes**" if result['p_value'] < 0.05 else "No"
        question_short = result['question'][:33]
        print(f"{question_short:<35} {result['chi2']:<10.4f} "
              f"{result['p_value']:<10.4f} {result['phi']:<10.4f} "
              f"{result['effect_size']:<15}")
    
    print("\n** Statistically significant at α = 0.05")
    
    # Response rate comparison
    print("\n" + "="*80)
    print("Response Rate Comparison")
    print("="*80)
    print(f"\n{'Question':<35} {'Large Box':<12} {'Small Box':<12} "
          f"{'Difference':<12}")
    print("-"*80)
    
    for result in all_results:
        large_rate = calculate_response_rate(
            result['large_box'][0], result['large_box'][1]
        )
        small_rate = calculate_response_rate(
            result['small_box'][0], result['small_box'][1]
        )
        diff = large_rate - small_rate
        
        question_short = result['question'][:33]
        print(f"{question_short:<35} {large_rate:>10.1f}% "
              f"{small_rate:>10.1f}% {diff:>+10.1f}%")


def print_effect_size_guide():
    """Print guide for interpreting Phi coefficient values."""
    print("\n" + "="*80)
    print("Effect Size Interpretation Guide (Phi Coefficient)")
    print("="*80)
    print("\n  < 0.10  : Negligible effect")
    print("  0.10-0.29 : Small effect")
    print("  0.30-0.49 : Medium effect")
    print("  ≥ 0.50  : Large effect")
    print("\nThe Phi coefficient measures the strength of association between")
    print("text box size and response rates, independent of sample size.")


def main():
    print("="*70)
    print("Chi-Square Test with Phi Coefficient: Text Box Size vs. Response Rate")
    print("="*70)
    print("\nHypothesis (H2): Larger text boxes will be associated with")
    print("fewer non-responses in open-ended questions.")
    
    # Load data
    print("\nLoading data from 'data/input/matrix-recoded.csv'...")
    matrix = pd.read_csv("../data/input/matrix-recoded.csv")
    print(f"Data loaded: {len(matrix)} records")
    
    questions_data = [
        ([53, 212], [39, 196], "Question 1: Problems or Negative Experiences"),
        ([64, 201], [43, 192], "Question 2: Additional Information"),
        ([52, 213], [30, 205], "Question 3: Suggestions for Improvement"),
        ([90, 169], [56, 175], "All Questions Combined (Total Sample)")
    ]
    
    # Perform chi-square tests with Phi calculation
    all_results = []
    
    for large_box, small_box, question_name in questions_data:
        results = perform_chi_square_with_phi(large_box, small_box, question_name)
        all_results.append(results)
        print_test_results(results)
    
    # Print comprehensive summary
    print_summary_table(all_results)
    print_effect_size_guide()
    
    # Overall conclusion
    print("\n" + "="*70)
    print("OVERALL CONCLUSION")
    print("="*70)
    
    significant_count = sum(1 for r in all_results if r['p_value'] < 0.05)
    total_count = len(all_results)
    avg_phi = np.mean([r['phi'] for r in all_results])
    
    print(f"\nSignificant results: {significant_count} out of {total_count} tests")
    print(f"Average Phi coefficient: {avg_phi:.4f} ({interpret_phi(avg_phi)} effect)")
    
    if significant_count > total_count / 2:
        print("\nThe majority of tests support the hypothesis that larger text boxes")
        print("are associated with higher response rates in open-ended questions.")
    elif significant_count > 0:
        print("\nMixed results: Some evidence supports the hypothesis, but not all")
        print("questions show a significant relationship.")
    else:
        print("\nThe hypothesis is not supported by the data.")
    
    # Effect size interpretation
    large_effects = sum(1 for r in all_results if r['phi'] >= 0.5)
    medium_effects = sum(1 for r in all_results if 0.3 <= r['phi'] < 0.5)
    small_effects = sum(1 for r in all_results if 0.1 <= r['phi'] < 0.3)
    
    if large_effects > 0 or medium_effects > 0:
        print(f"\nEffect sizes indicate practical significance:")
        if large_effects > 0:
            print(f"  - {large_effects} test(s) showed large effects")
        if medium_effects > 0:
            print(f"  - {medium_effects} test(s) showed medium effects")
        if small_effects > 0:
            print(f"  - {small_effects} test(s) showed small effects")
    
    print("\n" + "="*70)
    print("Analysis Complete!")
    print("="*70)


if __name__ == "__main__":
    main()
