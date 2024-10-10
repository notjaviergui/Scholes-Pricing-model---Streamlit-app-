import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import black_scholes
import streamlit as st

def generate_heatmap(S, K, T, r, sigma_range, S_range, option_type='call'):
    sigma_values = np.linspace(*sigma_range, 20)  # Reduced resolution for clearer ticks
    S_values = np.linspace(*S_range, 20)         # Reduced resolution for clearer ticks
    
    price_matrix = np.zeros((len(S_values), len(sigma_values)))
    
    for i, S_val in enumerate(S_values):
        for j, sigma_val in enumerate(sigma_values):
            price_matrix[i, j] = black_scholes(S_val, K, T, r, sigma_val, option_type)
    
    plt.figure(figsize=(12, 8))  # Increase figure size for better clarity
    
    sns.heatmap(price_matrix, xticklabels=np.round(sigma_values, 2), yticklabels=np.round(S_values, 2), cmap='RdYlGn', annot=True)
    
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.yticks(rotation=0)  # Ensure y-axis labels are horizontal

    plt.xlabel('Volatility (σ)')
    plt.ylabel('Stock Price (S)')
    plt.title(f'{option_type.capitalize()} Option Price Heatmap')
    
    st.pyplot(plt)