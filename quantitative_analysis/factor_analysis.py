"""
Exploratory Factor Analysis (EFA) for Questionnaire Data.

This script performs EFA on survey data to identify underlying factor structures
across different questionnaire formats and question ordering conditions.

Analysis includes:
- Bartlett's test of sphericity
- Kaiser-Meyer-Olkin (KMO) measure of sampling adequacy
- Factor analysis with Varimax rotation
- Scree plot visualization
- Factor loadings export
"""

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from factor_analyzer import (
    FactorAnalyzer,
    calculate_bartlett_sphericity,
    calculate_kmo
)

# Constants
DATA_FILEPATH = "../data/input/matrix-final.csv"
OUTPUT_FILEPATH = "data/output/loadings{}.csv"
STUDENT_ROLE_CODE = 2
FREQUENT_VISITOR_THRESHOLD = 1
HIDDEN_THRESHOLD = 50
NUM_FACTORS = 3
NUM_GROUPS = 4

# Question columns for analysis
QUESTION_COLS = [
    'g01', 'g02', 'g03', 'g04', 'g05', 'g06',
    'g07', 'g08', 'g09', 'g10', 'g11', 'g12'
]

# Group labels for visualization
GROUP_LABELS = [
    'Single Page - Order A',
    'Single Page - Order B',
    'Slides - Order A',
    'Slides - Order B'
]

# ANSI color codes for terminal output
COLOR_CYAN = '\033[96m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RED = '\033[91m'
COLOR_RESET = '\033[0m'

def filter_data(matrix):
    """
    Load data and filter for students who frequently visit.
    
    Args:
        matrix: DataFrame with survey data
        
    Returns:
        DataFrame: Filtered data containing only students who frequently visit
    """
    
    initial_count = len(matrix)
    
    # Filter for students only
    matrix = matrix[matrix['uloga'] == STUDENT_ROLE_CODE]
    students_count = len(matrix)
    
    # Filter for frequent visitors
    matrix = matrix[matrix['cesto'] > FREQUENT_VISITOR_THRESHOLD]
    final_count = len(matrix)
    
    print(f"Initial records: {initial_count}")
    print(f"Students only: {students_count}")
    print(f"Frequent visitors: {final_count}")
    
    if matrix.empty:
        print(f"{COLOR_RED}Error: No data left after filtering.{COLOR_RESET}")
        return pd.DataFrame()
    
    return matrix


def prepare_format_groups(matrix):
    """
    Split data into 4 groups based on format and question order.
    
    Groups:
    1. Format 1 (single page), Order A (hidden < 51)
    2. Format 1 (single page), Order B (hidden > 50)
    3. Format 2 (slides), Order A (hidden < 51)
    4. Format 2 (slides), Order B (hidden > 50)
    
    Args:
        matrix: Filtered DataFrame
        
    Returns:
        list: List of 4 DataFrames, one for each group
    """
    print(f"\n{COLOR_CYAN}Preparing format groups...{COLOR_RESET}")
    
    # Select relevant columns
    cols = ['formatUp', 'hidden'] + QUESTION_COLS
    grid = matrix[cols].copy()
    
    # Create 4 groups
    groups = []
    conditions = [
        (grid['formatUp'] == 1) & (grid['hidden'] < HIDDEN_THRESHOLD + 1),
        (grid['formatUp'] == 1) & (grid['hidden'] > HIDDEN_THRESHOLD),
        (grid['formatUp'] == 2) & (grid['hidden'] < HIDDEN_THRESHOLD + 1),
        (grid['formatUp'] == 2) & (grid['hidden'] > HIDDEN_THRESHOLD)
    ]
    
    for i, condition in enumerate(conditions):
        group = grid[condition].copy()
        group.drop(['formatUp', 'hidden'], axis=1, inplace=True)
        groups.append(group)
        print(f"  Group {i + 1} ({GROUP_LABELS[i]}): {len(group)} records")
    
    return groups


def perform_adequacy_tests(matrix):
    """
    Perform Bartlett's sphericity test and KMO test.
    
    Args:
        matrix: DataFrame with survey data
        
    Returns:
        tuple: (chi_square, p_value, kmo_model)
    """
    print(f"\n{COLOR_CYAN}Performing adequacy tests...{COLOR_RESET}")
    
    # Select question columns and remove missing values
    cols =  QUESTION_COLS
    grid = matrix[cols].copy()
    faktor = grid.dropna()

    
    print(f"Complete cases for analysis: {len(faktor)}")
    
    # Bartlett's test of sphericity
    chi_square, p_value = calculate_bartlett_sphericity(faktor)
    print(f"\n{COLOR_GREEN}Bartlett's Test of Sphericity:{COLOR_RESET}")
    print(f"  Chi-square: {chi_square:.2f}")
    print(f"  p-value: {p_value:.4e}")
    
    if p_value < 0.001:
        print(f"  {COLOR_GREEN}✓ Data is suitable for factor analysis (p < 0.001){COLOR_RESET}")
    else:
        print(f"  {COLOR_YELLOW}⚠ Warning: p-value > 0.001{COLOR_RESET}")
    
    # Kaiser-Meyer-Olkin (KMO) test
    kmo_all, kmo_model = calculate_kmo(faktor)
    print(f"\n{COLOR_GREEN}Kaiser-Meyer-Olkin (KMO) Test:{COLOR_RESET}")
    print(f"  Overall KMO: {kmo_model:.3f}")
    
    if kmo_model >= 0.9:
        interpretation = "Marvelous"
    elif kmo_model >= 0.8:
        interpretation = "Meritorious"
    elif kmo_model >= 0.7:
        interpretation = "Middling"
    elif kmo_model >= 0.6:
        interpretation = "Mediocre"
    elif kmo_model >= 0.5:
        interpretation = "Miserable"
    else:
        interpretation = "Unacceptable"
    
    print(f"  Interpretation: {interpretation}")
    
    return chi_square, p_value, kmo_model


def perform_factor_analysis(groups):
    """
    Perform factor analysis on all groups.
    
    Args:
        groups: List of DataFrames for each group
        
    Returns:
        tuple: (loadings, eigenvalues)
    """
    print(f"\n{COLOR_CYAN}Performing factor analysis...{COLOR_RESET}")
    
    loadings = []
    eigenvalues = []
    
    for i, group in enumerate(groups):
        print(f"  Analyzing Group {i + 1} ({GROUP_LABELS[i]})...")
        
        fa = FactorAnalyzer(
            rotation='varimax',
            method='principal',
            impute='drop',
            n_factors=NUM_FACTORS
        )
        fa.fit(group)
        
        loadings.append(fa.loadings_)
        ev, _ = fa.get_eigenvalues()
        eigenvalues.append(ev)
        
        print(f"    Eigenvalues (first 3): {ev[:3]}")
    
    return loadings, eigenvalues


def create_scree_plot(eigenvalues, groups):
    """
    Create and display scree plot for all groups.
    
    Args:
        eigenvalues: List of eigenvalue arrays
        groups: List of DataFrames for determining number of factors
    """
    print(f"\n{COLOR_CYAN}Creating scree plot...{COLOR_RESET}")
    
    plt.figure(figsize=(10, 6))
    
    for i, (ev, group) in enumerate(zip(eigenvalues, groups)):
        num_factors = group.shape[1]
        plt.plot(range(1, num_factors + 1), ev, '-o', label=GROUP_LABELS[i])
    
    plt.title('Scree Plot - Eigenvalues by Factor', fontsize=14, fontweight='bold')
    plt.xlabel('Factor Number', fontsize=12)
    plt.ylabel('Eigenvalue', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    plt.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='Kaiser criterion (eigenvalue = 1)')
    plt.tight_layout()
    plt.show()


def save_loadings_to_csv(loadings, group_index):
    """
    Save factor loadings to CSV file.
    
    Args:
        loadings: Array of factor loadings
        group_index: Index of the group (0-3)
    """
    print(f"\n{COLOR_CYAN}Saving factor loadings to CSV...{COLOR_RESET}")
    
    # Round to 2 decimals and convert to string
    loadings_formatted = np.round(loadings, 2).astype(str)
    
    # Insert question names as first column
    loadings_formatted = np.insert(
        loadings_formatted, 0, QUESTION_COLS, axis=1
    )
    
    # Insert header row
    header = [""] + [f"F{i+1}" for i in range(NUM_FACTORS)]
    loadings_formatted = np.insert(
        loadings_formatted, 0, header, axis=0
    )
    
    # Save to CSV
    output_path = OUTPUT_FILEPATH.format(group_index)
    with open(output_path, "w+", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(loadings_formatted)
    
    print(f"Factor loadings saved to: {output_path}")


def create_loadings_heatmaps(loadings):
    """
    Create heatmap visualizations for factor loadings of all groups.
    
    Args:
        loadings: List of factor loading arrays for each group
    """
    print(f"\n{COLOR_CYAN}Creating factor loadings heatmaps...{COLOR_RESET}")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()
    
    factor_labels = [f"F{i+1}" for i in range(NUM_FACTORS)]
    
    for i, (loading, ax) in enumerate(zip(loadings, axes)):
        # Create DataFrame for heatmap
        loading_df = pd.DataFrame(
            np.round(loading, 2),
            index=QUESTION_COLS,
            columns=factor_labels
        )
        
        # Create heatmap
        sns.heatmap(
            loading_df,
            ax=ax,
            cmap='RdBu_r',
            center=0,
            vmin=-1,
            vmax=1,
            annot=True,
            fmt='.2f',
            square=False,
            cbar_kws={"shrink": 0.8}
        )
        
        ax.set_title(GROUP_LABELS[i], fontsize=12, fontweight='bold')
        ax.set_xlabel('Factors', fontsize=10)
        ax.set_ylabel('Items', fontsize=10)
    
    plt.suptitle('Factor Loadings by Group', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


def print_summary(chi_square, p_value, kmo_model, eigenvalues):
    """
    Print summary of factor analysis results.
    
    Args:
        chi_square: Bartlett's chi-square statistic
        p_value: Bartlett's p-value
        kmo_model: Overall KMO measure
        eigenvalues: List of eigenvalue arrays
    """
    print(f"\n{'=' * 70}")
    print(f"{COLOR_GREEN}ANALYSIS SUMMARY{COLOR_RESET}")
    print(f"{'=' * 70}")
    
    print(f"\n{COLOR_CYAN}Data Adequacy:{COLOR_RESET}")
    print(f"  Bartlett's χ²: {chi_square:.2f}, p = {p_value:.4e}")
    print(f"  KMO: {kmo_model:.3f}")
    
    print(f"\n{COLOR_CYAN}Factor Structure:{COLOR_RESET}")
    print(f"  Number of factors extracted: {NUM_FACTORS}")
    
    for i, ev in enumerate(eigenvalues):
        print(f"\n  {GROUP_LABELS[i]}:")
        for j in range(NUM_FACTORS):
            variance_explained = (ev[j] / len(QUESTION_COLS)) * 100
            print(f"    Factor {j+1}: λ = {ev[j]:.3f} ({variance_explained:.1f}% variance)")
    
    print(f"\n{'=' * 70}")


def main():
    print("="*70)
    print("Exploratory Factor Analysis (EFA) for Questionnaire Data")
    print("="*70)
    print("\nThis analysis performs EFA on survey data to identify underlying")
    print("factor structures across different questionnaire formats.")
    
    # Load data
    print(f"\nLoading data from '{DATA_FILEPATH}'...")
    matrix = pd.read_csv(DATA_FILEPATH)
    print(f"Data loaded: {len(matrix)} records")
    
    # Filter data
    filtered_matrix = filter_data(matrix)
    if filtered_matrix.empty:
        return
    
    # Prepare format groups
    groups = prepare_format_groups(filtered_matrix)
    
    # Check if any group is empty
    if any(len(group) == 0 for group in groups):
        print(f"{COLOR_RED}Error: One or more groups have no data.{COLOR_RESET}")
        return
    
    # Perform adequacy tests
    chi_square, p_value, kmo_model = perform_adequacy_tests(filtered_matrix)
    
    # Perform factor analysis
    loadings, eigenvalues = perform_factor_analysis(groups)
    
    # Create scree plot
    create_scree_plot(eigenvalues, groups)
    
    # Create factor loadings heatmaps
    create_loadings_heatmaps(loadings)
    
    # Save loadings for all groups to CSV
    save_loadings_to_csv(loadings[0], 0)
    save_loadings_to_csv(loadings[1], 1)
    save_loadings_to_csv(loadings[2], 2)
    save_loadings_to_csv(loadings[3], 3)
    
    # Print summary
    print_summary(chi_square, p_value, kmo_model, eigenvalues)
    
    print(f"\n{COLOR_GREEN}Analysis complete!{COLOR_RESET}")


if __name__ == "__main__":
    main()

