import sys

sys.path.append("/Users/johnlevy/Code/quant_projects/learning_finance")

from scipy import stats
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.models.black_scholes import (
    black_scholes_call,
    black_scholes_put,
    delta_call,
    gamma,
    theta_call,
    vega,
    rho_call,
    delta_put,
    theta_put,
    rho_put,
)

# Streamlit app title
st.set_page_config(page_title="Black-Scholes Option Pricing", layout="wide")
st.title("Black-Scholes Option Pricing")

# Top sliders sectioon
st.header("Input Parameters")

slider_row_col1, slider_row_col2, slider_row_col3 = st.columns([1, 1, 1])

with slider_row_col1:
    S = st.slider("Stock Price (S)", min_value=10, max_value=500, value=100)
with slider_row_col2:
    K = st.slider("Strike Price (K)", min_value=10, max_value=500, value=100)
with slider_row_col3:
    T = st.slider("Time to Expiration (T in years)", min_value=1, max_value=10, value=1)

slider_row2_col1, slider_row2_col2 = st.columns([1, 1])

with slider_row2_col1:
    r = st.slider(
        "Risk-Free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.01
    )
with slider_row2_col2:
    sigma = st.slider(
        "Volatility (σ)", min_value=0.1, max_value=1.0, value=0.2, step=0.01
    )

# Compute option prices
call_price = black_scholes_call(S, K, T, r, sigma)
put_price = black_scholes_put(S, K, T, r, sigma)

# Calculate the Greeks for Call and Put options
call_delta = delta_call(S, K, T, r, sigma)
call_gamma = gamma(S, K, T, r, sigma)
call_theta = theta_call(S, K, T, r, sigma)
call_vega = vega(S, K, T, r, sigma)
call_rho = rho_call(S, K, T, r, sigma)

put_delta = delta_put(S, K, T, r, sigma)
put_gamma = gamma(S, K, T, r, sigma)
put_theta = theta_put(S, K, T, r, sigma)
put_vega = vega(S, K, T, r, sigma)
put_rho = rho_put(S, K, T, r, sigma)

# Option prices section
call_col, put_col = st.columns([1, 1])

with call_col:
    st.header("Call Option Price")
    st.markdown(
        f"""
        <div style="padding: 20px; border-radius: 10px; background-color: #d4edda; color: #155724; font-size: 20px; text-align: center;">
            <b>${call_price:.2f}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Option Greeks for Call Option")
    st.markdown(
        f"""
        <div style="padding: 20px; border-radius: 10px; background-color: #d4edda; color: #155724; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Delta (Δ): {call_delta:.4f}</b>
        </div>
        <div style="padding: 20px; border-radius: 10px; background-color: #d4edda; color: #155724; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Gamma (Γ): {call_gamma:.4f}</b>
        </div>
        <div style="padding: 20px; border-radius: 10px; background-color: #d4edda; color: #155724; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Theta (Θ): {call_theta:.4f}</b>
        </div>
        <div style="padding: 20px; border-radius: 10px; background-color: #d4edda; color: #155724; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Vega (ν): {call_vega:.4f}</b>
        </div>
        <div style="padding: 20px; border-radius: 10px; background-color: #d4edda; color: #155724; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Rho (ρ): {call_rho:.4f}</b>
        </div>
    """,
        unsafe_allow_html=True,
    )


with put_col:
    st.header("Put Option Price")
    st.markdown(
        f"""
        <div style="padding: 20px; border-radius: 10px; background-color: #f8d7da; color: #721c24; font-size: 20px; text-align: center;">
            <b>${put_price:.2f}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Option Greeks for Put Option")
    st.markdown(
        f"""
        <div style="padding: 20px; border-radius: 10px; background-color: #f8d7da; color: #721c24; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Delta (Δ): {put_delta:.4f}</b>
        </div>
        <div style="padding: 20px; border-radius: 10px; background-color: #f8d7da; color: #721c24; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Gamma (Γ): {put_gamma:.4f}</b>
        </div>
        <div style="padding: 20px; border-radius: 10px; background-color: #f8d7da; color: #721c24; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Theta (Θ): {put_theta:.4f}</b>
        </div>
        <div style="padding: 20px; border-radius: 10px; background-color: #f8d7da; color: #721c24; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Vega (ν): {put_vega:.4f}</b>
        </div>
        <div style="padding: 20px; border-radius: 10px; background-color: #f8d7da; color: #721c24; font-size: 20px; text-align: center; margin-bottom: 20px;">
            <b>Rho (ρ): {put_rho:.4f}</b>
        </div>
    """,
        unsafe_allow_html=True,
    )
