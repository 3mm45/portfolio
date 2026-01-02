"""
Survey Response Length Analysis by Format.

This module analyzes response length differences between survey formats
and performs statistical tests including ANOVA, Mann-Whitney U, t-tests,
chi-square, and SEM analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.graphics.factorplots import interaction_plot
from scipy.stats import mannwhitneyu, ttest_ind, chi2_contingency
from semopy import Model, Optimizer, gather_statistics

def classify_text_box_size(hidden_value):
    """Classify text box size based on hidden value.
    
    Args:
        hidden_value: Hidden field value from survey
        
    Returns:
        1 for smaller box (hidden < 51), 2 for larger box (hidden >= 51)
    """
    return 1 if hidden_value < 51 else 2


def calculate_response_lengths(df):
    """Calculate response lengths for text fields.
    
    Args:
        df: DataFrame with survey responses
        
    Returns:
        DataFrame with added response length columns
    """
    # Initialize length columns
    df['duzodg'] = 0
    df['duzodgm'] = 0
    df['duzodgv'] = 0
    
    # Convert text columns to strings
    txt_columns = ['txt01', 'txt02', 'txt03', 'txt01mali', 'txt02mali', 'txt03mali']
    for col in txt_columns:
        df[col] = df[col].astype(str)
    
    # Calculate maximum length for large and small text boxes
    df['duzodgv'] = np.maximum(
        df['txt01'].str.len(),
        np.maximum(df['txt02'].str.len(), df['txt03'].str.len())
    )
    
    df['duzodgm'] = np.maximum(
        df['txt01mali'].str.len(),
        np.maximum(df['txt02mali'].str.len(), df['txt03mali'].str.len())
    )
    
    # Set length to 0 if less than threshold (10 characters)
    min_length_threshold = 10
    df['duzodgv'] = df['duzodgv'].apply(
        lambda x: 0 if x < min_length_threshold else x
    )
    df['duzodgm'] = df['duzodgm'].apply(
        lambda x: 0 if x < min_length_threshold else x
    )
    
    # Total response length
    df['duzodg'] = df['duzodgv'] + df['duzodgm']
    
    return df


def add_response_flags(df):
    """Add flags for response completeness.
    
    Args:
        df: DataFrame with survey responses
        
    Returns:
        DataFrame with added flag columns
    """
    # Flag: answered at least one text box
    df['imaot'] = df['duzodg'].apply(lambda x: 1 if x > 0 else 0)
    
    # Flag: answered all grid questions (validity check)
    df['imasve'] = df.iloc[:, 7:20].sum(axis=1, min_count=13)
    
    return df


def filter_valid_responses(df, min_response_length=30):
    """Filter for valid responses with complete data.
    
    Args:
        df: DataFrame with survey responses
        min_response_length: Minimum response length to include
        
    Returns:
        Filtered DataFrame with valid responses only
    """
    # Filter for complete grid responses and valid time
    filtered = df[(~df['imasve'].isna()) & (df['vreme'] > 1)].copy()
    
    # Further filter by minimum response length
    filtered = filtered[filtered['duzodg'] > min_response_length]
    
    return filtered


def create_format_labels(df):
    """Create human-readable labels for format types.
    
    Args:
        df: DataFrame with formatUp column
        
    Returns:
        DataFrame with added label columns
    """

    format_map = {
        1: "Single Page",
        2: "Slides"
    }
    
    textbox_size_map = {
        1: "Small",
        2: "Large"
    }
    
    df['format_label'] = df['formatUp'].map(
        lambda x: format_map.get(x, "Unknown")
    )

    df['Text Box Size'] = df['dugi'].map(
        lambda x: textbox_size_map.get(x, "Unknown")
    )
    
    return df


def plot_interaction(df):
    """Create interaction plot for response length by format and textbox size."""
    format_labels = df['format_label'].array
    
    fig = interaction_plot(
        format_labels,
        df['Text Box Size'],
        df['duzodg'],
        colors=['red', 'blue'],
        markers=['D', '^'],
        ms=10,
        ylabel="Response Length",
        xlabel="Survey Format"
    )
    plt.show()


def perform_anova(df):
    """Perform ANOVA analysis on response length."""
    print("\n" + "="*50)
    print("ANOVA Analysis")
    print("="*50)
    
    model = ols('duzodg ~ C(formatUp) + C(dugi) + C(formatUp):C(dugi)', data=df).fit()
    anova_results = sm.stats.anova_lm(model, typ=3)
    
    print(anova_results)
    print("\n" + model.summary().as_text())

    print("\n ANOVA END")

def calculate_mean_by_format(df):
    """Calculate and print mean response lengths by format."""
    print("\n" + "="*50)
    print("Mean Response Lengths by Format")
    print("="*50)
    
    form1_mean = df[(df['formatUp'] == 1) & (df['duzodg'] > 0)]['duzodg'].mean()
    form2_mean = df[(df['formatUp'] == 2) & (df['duzodg'] > 0)]['duzodg'].mean()
    
    print(f"Format 1 (Jedna strana): {form1_mean:.2f}")
    print(f"Format 2 (Slajdovi): {form2_mean:.2f}")


def perform_mann_whitney_test(form1, form2):
    """Perform Mann-Whitney U test between two formats."""
    print("\n" + "="*50)
    print("Mann-Whitney U Test")
    print("="*50)
    
    u_stat, p_value = mannwhitneyu(form1['duzodg'], form2['duzodg'])
    print(f"U statistic: {u_stat:.2f}")
    print(f"p-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("Result: Statistically significant difference (p < 0.05)")
    else:
        print("Result: No statistically significant difference (p >= 0.05)")


def perform_t_test(form1, form2):
    """Perform independent t-test between two formats."""
    print("\n" + "="*50)
    print("Independent T-Test")
    print("="*50)
    
    t_stat, p_val = ttest_ind(form1['duzodg'], form2['duzodg'], equal_var=False)
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_val:.4f}")
    
    if p_val < 0.05:
        print("Result: Statistically significant difference (p < 0.05)")
    else:
        print("Result: No statistically significant difference (p >= 0.05)")


def perform_chi_square_test(df):
    """Perform chi-square test if required column exists."""
    print("\n" + "="*50)
    print("Chi-Square Test")
    print("="*50)
    
    if 'zaAnalytics1[SQ001]' in df.columns:
        proba = pd.crosstab(
            index=df['imaot'],
            columns=df['zaAnalytics1[SQ001]']
        )
        stat, p_value, dof, expected = chi2_contingency(proba)
        print(f"Chi-square statistic: {stat:.4f}")
        print(f"p-value: {p_value:.4f}")
        print(f"Degrees of freedom: {dof}")
    else:
        print("Skipped: Column 'zaAnalytics1[SQ001]' not found in data")


def perform_sem_analysis(df):
    """Perform Structural Equation Modeling (SEM) analysis."""
    print("\n" + "="*50)
    print("SEM Analysis")
    print("="*50)
    
    required_cols = ['g01', 'g02', 'g03', 'g04', 'g05', 'g06',
                     'g07', 'g08', 'g09', 'g10', 'g11', 'g12']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"Skipped: Missing columns {missing_cols}")
        return
    
    # Prepare dataset
    faktor = df[required_cols].dropna()
    
    if len(faktor) < 10:
        print(f"Skipped: Insufficient data ({len(faktor)} complete rows, need >= 10)")
        return
    
    print(f"Running SEM with {len(faktor)} observations...")
    
    model_spec = '''
        F1 =~ g02 + g03 + g04 + g11
        F2 =~ g01 + g05 + g12
        F3 =~ g06 + g07 + g08 + g09
    '''
    
    model = Model(model_spec)
    model.load_dataset(faktor)
    
    opt = Optimizer(model)
    ofv = opt.optimize()
    stats = gather_statistics(opt)
    
    print("\nModel Statistics:")
    print(stats)
    
    if 'rmsea' in stats:
        print(f"\nRMSEA: {stats['rmsea']:.4f}")


def main():
    print("="*70)
    print("Survey Response Length Analysis by Format")
    print("="*70)
    print("\nThis analysis examines response length differences between survey formats")
    print("and performs statistical tests including ANOVA, Mann-Whitney U, and t-tests.")
    
    # Load data
    print("\nLoading data from 'data/input/matrix-final.csv'...")
    matrix = pd.read_csv("../data/input/matrix-final.csv")
    print(f"Data loaded: {len(matrix)} records")
    
    # Classify text box sizes
    matrix['dugi'] = matrix['hidden'].apply(classify_text_box_size)
    
    # # Calculate response lengths
    matrix = calculate_response_lengths(matrix)
    
    # # Add response flags
    matrix = add_response_flags(matrix)
    
    # Filter for valid responses
    samosvi = filter_valid_responses(matrix, min_response_length=30)
    
    # Create labels for visualization
    samosvi = create_format_labels(samosvi)
    
    print(f"\nTotal valid responses: {len(samosvi)}")
    print("\nTextbox size distribution:")
    print(samosvi['dugi'].value_counts().sort_index())
    
    # Visualization
    print("\nGenerating interaction plot...")
    plot_interaction(samosvi)
    
    # Statistical analyses
    perform_anova(samosvi)
    calculate_mean_by_format(matrix)
    
    print("\n" + "="*70)
    print("Analysis Complete!")
    print("="*70)


if __name__ == "__main__":
    main()
