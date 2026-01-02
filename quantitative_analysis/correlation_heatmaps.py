"""
Correlation matrix analysis and visualization.

This module performs bootstrap correlation analysis and generates heatmaps
for different survey format configurations.
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats


def filter_data(matrix):
    """Load survey data and filter for students who regularly visit."""
    # Filter: only students who regularly visit
    matrix = matrix[matrix['uloga'] == 2]
    matrix = matrix[matrix['cesto'] > 1]
    return matrix


def prepare_format_groups(matrix):
    """Split data into 4 format groups based on formatUp and hidden values."""
    columns = ['formatUp', 'hidden', 'g01', 'g02', 'g03', 'g04', 'g05', 'g06',
               'g07', 'g08', 'g09', 'g10', 'g11', 'g12']
    grid = matrix[columns]
    
    forms = [
        grid[(grid['formatUp'] == 1) & (grid['hidden'] < 51)].copy(),
        grid[(grid['formatUp'] == 1) & (grid['hidden'] > 50)].copy(),
        grid[(grid['formatUp'] == 2) & (grid['hidden'] < 51)].copy(),
        grid[(grid['formatUp'] == 2) & (grid['hidden'] > 50)].copy()
    ]
    
    # Drop grouping columns
    for form in forms:
        form.drop(["formatUp", "hidden"], axis=1, inplace=True)
    
    return forms


def get_upper_triangle(df):
    """Extract upper triangle values from a correlation matrix."""
    if not isinstance(df, np.ndarray):
        if isinstance(df, pd.DataFrame):
            df = df.values
        else:
            raise TypeError('Must be np.ndarray or pd.DataFrame')
    
    mask = np.triu_indices(df.shape[0], k=1)
    return df[mask]


def bootstrap_correlation(mat1, mat2):
    """Calculate correlation between two matrices using bootstrap sampling."""
    df_1 = mat1.sample(frac=0.6)
    df_2 = mat2.sample(frac=0.6)
    corr_m1 = df_1.corr(method='kendall')
    corr_m2 = df_2.corr(method='kendall')
    res = stats.kendalltau(get_upper_triangle(corr_m1), get_upper_triangle(corr_m2))
    return res.statistic


def run_bootstrap_analysis(forms, n_iterations=1000):
    """Run bootstrap analysis for all format combinations."""
    print("\n#6 - Bootstrap Analysis")
    print("Format pairs: CI 2.5%, Mean, CI 97.5%")
    
    for a in range(4):
        for b in range(a, 4):
            # First bootstrap run
            bootr = [bootstrap_correlation(forms[a], forms[b]) 
                     for _ in range(n_iterations)]
            
            print(f"{a} {b} "
                  f"{np.percentile(bootr, 2.5):.2f} "
                  f"{np.mean(bootr):.2f} "
                  f"{np.percentile(bootr, 97.5):.2f}")
            
            # Second bootstrap run
            bootr = [bootstrap_correlation(forms[a], forms[b]) 
                     for _ in range(n_iterations)]
            
            print(f"{a} {b} "
                  f"{np.percentile(bootr, 2.5):.2f} "
                  f"{np.mean(bootr):.2f} "
                  f"{np.percentile(bootr, 97.5):.2f}")
            print("***************")


def calculate_correlations(forms):
    """Calculate Spearman correlations for each format."""
    correlations = [form.corr(method='spearman') for form in forms]
    
    # Reorder columns for formats 2 and 4
    column_order = ['g02', 'g11', 'g04', 'g01', 'g05', 'g09', 
                    'g07', 'g03', 'g08', 'g10', 'g06', 'g12']
    corr_m2_ordered = forms[1][column_order].corr(method='spearman')
    corr_m4_ordered = forms[3][column_order].corr(method='spearman')
    
    return correlations, corr_m2_ordered, corr_m4_ordered


def plot_individual_heatmaps(correlations, corr_m2_ordered, corr_m4_ordered):
    """Plot 2x2 grid of heatmaps for individual format configurations."""
    print("\n#7 - Generating heatmaps")
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 20))
    sns.set_style("white")
    
    heatmap_params = {
        'cmap': 'RdBu_r',
        'center': 0,
        'vmin': -1,
        'vmax': 1,
        'square': True,
        'annot' : True, # 'annot' : True, Adding values to labels
        'fmt' : '.2f',
        'cbar_kws': {"shrink": 0.5},
        'xticklabels': True
     }
    
    sns.heatmap(correlations[0], ax=axes[0, 0], **heatmap_params)
    axes[0, 0].set_title('Single Page - Order A',fontweight='bold')
    
    sns.heatmap(corr_m2_ordered, ax=axes[0, 1], **heatmap_params)
    axes[0, 1].set_title('Single Page - Order B',fontweight='bold')
    
    sns.heatmap(correlations[2], ax=axes[1, 0], **heatmap_params)
    axes[1, 0].set_title('Slides - Order A',fontweight='bold')
    
    sns.heatmap(corr_m4_ordered, ax=axes[1, 1], **heatmap_params)
    axes[1, 1].set_title('Slides - Order B',fontweight='bold')
    
    plt.tight_layout()
    plt.show()


def main():
    print("="*70)
    print("Correlation Matrix Analysis and Visualization")
    print("="*70)
    print("\nThis analysis performs bootstrap correlation analysis and generates")
    print("heatmaps for different survey format configurations.")
    
    # Load data
    print("\nLoading data from 'data/input/matrix-final.csv'...")
    filtered_matrix = pd.read_csv("../data/input/matrix-final.csv")
    print(f"Data loaded: {len(filtered_matrix)} records")
    
    # Filter and prepare data
    filtered_matrix = filter_data(filtered_matrix)
    print(f"After filtering (students who regularly visit): {len(filtered_matrix)} records")
    
    forms = prepare_format_groups(filtered_matrix)
    
    # Run bootstrap analysis
    #run_bootstrap_analysis(forms)
    
    # Calculate correlations
    correlations, corr_m2_ordered, corr_m4_ordered = calculate_correlations(forms)
    
    # Generate visualizations
    plot_individual_heatmaps(correlations, corr_m2_ordered, corr_m4_ordered)


if __name__ == "__main__":
    main()
