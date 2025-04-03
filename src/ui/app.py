import sys

sys.path.append("/Users/johnlevy/Code/quant_projects/option_pricer")

import streamlit as st
from src.models.black_scholes import black_scholes_call, black_scholes_put

# Streamlit app title
st.title("Black-Scholes Option Pricing")

# User inputs for option parameters
S = st.slider("Stock Price (S)", min_value=10, max_value=500, value=100)
K = st.slider("Strike Price (K)", min_value=10, max_value=500, value=100)
T = st.slider("Time to Expiration (T in years)", min_value=1, max_value=10, value=1)
r = st.slider("Risk-Free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.01)
sigma = st.slider(
    "Volatility (sigma)", min_value=0.1, max_value=1.0, value=0.2, step=0.01
)

# Compute option prices
call_price = black_scholes_call(S, K, T, r, sigma)
put_price = black_scholes_put(S, K, T, r, sigma)

# Display results
st.write(f"### Call Option Price: ${call_price:.2f}")
st.write(f"### Put Option Price: ${put_price:.2f}")
