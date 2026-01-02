"""
Inter-item correlation (IAK) analysis.

This module calculates inter-item correlations for g01-g13 items.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

vars = ['g01', 'g02', 'g03', 'g04', 'g05', 'g06', 'g07', 'g08', 
            'g09', 'g10', 'g11', 'g12', 'g13']


def filter_data(matrix):
    """Filter for students who regularly visit."""
    matrix = matrix[matrix['uloga'] == 2]  # Only students
    matrix = matrix[matrix['cesto'] > 1]   # Only those who regularly visit the website
    # Filter rows where at least 5 fields from g01-g13 have values
    matrix = matrix[matrix[vars].notna().sum(axis=1) >= 6]
    return matrix

def calculate_iic(grid):
    """
    Calculate inter-item correlations for all items.
    
    Returns:
        pd.DataFrame: Correlation matrix
    """
    print("\n" + "="*70)
    print("Inter-item Correlation (IAK)")
    print("="*70)
    
    # Calculate inter-item correlations
    correlations = grid.corr().round(2)
    mean_iic = correlations.mean().mean()
    print(f"Mean IAC: {mean_iic:.2f}")
    
    return correlations


def create_iac_heatmap(correlations):
    """
    Create heatmap visualization for inter-item correlations.
    
    Args:
        correlations: DataFrame with correlation matrix
    """
    print("\nCreating inter-item correlation heatmap...")
    
    plt.figure(figsize=(12, 10))
    
    sns.heatmap(
        correlations,
        cmap='RdBu_r',
        center=0,
        vmin=-1,
        vmax=1,
        annot=True,
        fmt='.2f',
        square=True,
        cbar_kws={"shrink": 0.8},
        linewidths=0.5
    )
    
    plt.title('Inter-item Correlation Matrix (g01-g13)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def main():
    print("="*70)
    print("Inter-Item Correlation (IAK) Analysis")
    print("="*70)
    print("\nThis analysis calculates inter-item correlations for g01-g13 items.")
    
    # Load data
    print("\nLoading data from 'data/input/matrix-final.csv'...")
    matrix = pd.read_csv("data/input/matrix-final.csv")
    print(f"Data loaded: {len(matrix)} records")
    
    # Filter data
    filtered_matrix = filter_data(matrix)
    print(f"After filtering (students who regularly visit): {len(filtered_matrix)} records")
    
    grid = filtered_matrix[vars]
    
    # Calculate inter-item correlations
    correlations = calculate_iic(grid)
    
    # Create heatmap visualization
    create_iac_heatmap(correlations)
    
    # Save correlation matrix to CSV
    output_csv = "data/output/iic_all_formats.csv"
    correlations.to_csv(output_csv)
    print(f"\nInter-item correlation matrix saved to {output_csv}")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
