import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.models.black_scholes import black_scholes_call, black_scholes_put

# Streamlit page configuration
st.set_page_config(page_title="Option Sensitivity Analysis", layout="wide")
st.title("Option Sensitivity Analysis")

# Fixed parameter selection
st.header("Select Fixed Parameters")
S_fixed = st.slider("Stock Price (S)", min_value=10, max_value=500, value=100)
K_fixed = st.slider("Strike Price (K)", min_value=10, max_value=500, value=100)
T_fixed = st.slider(
    "Time to Expiration (T in years)", min_value=1, max_value=10, value=1
)
r_fixed = st.slider(
    "Risk-Free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.01
)
sigma_fixed = st.slider(
    "Volatility (σ)", min_value=0.1, max_value=1.0, value=0.2, step=0.01
)

st.divider()


# Function to create sensitivity plots
def create_sensitivity_plot(param_name, param_values, fixed_params):
    call_prices = [
        black_scholes_call(
            fixed_params["S"],
            fixed_params["K"],
            fixed_params["T"],
            fixed_params["r"],
            fixed_params["sigma"],
        )
        for fixed_params[param_name] in param_values
    ]
    put_prices = [
        black_scholes_put(
            fixed_params["S"],
            fixed_params["K"],
            fixed_params["T"],
            fixed_params["r"],
            fixed_params["sigma"],
        )
        for fixed_params[param_name] in param_values
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=param_values,
            y=call_prices,
            mode="lines",
            name="Call Price",
            line=dict(color="green"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=param_values,
            y=put_prices,
            mode="lines",
            name="Put Price",
            line=dict(color="red"),
        )
    )

    fig.update_layout(
        title=f"Option Prices vs. {param_name}",
        xaxis_title=param_name,
        yaxis_title="Option Price",
        legend_title="Option Type",
    )

    return fig


# Create individual sections for each varying parameter
param_names = ["S", "K", "T", "r", "sigma"]
param_labels = {
    "S": "Stock Price",
    "K": "Strike Price",
    "T": "Time to Expiration",
    "r": "Risk-Free Rate",
    "sigma": "Volatility",
}
param_ranges = {
    "S": np.linspace(10, 500, 100),
    "K": np.linspace(10, 500, 100),
    "T": np.linspace(0.1, 10, 100),
    "r": np.linspace(0.0, 0.2, 100),
    "sigma": np.linspace(0.1, 1.0, 100),
}

for param in param_names:
    st.subheader(f"Effect of {param_labels[param]}")
    fixed_params = {
        "S": S_fixed,
        "K": K_fixed,
        "T": T_fixed,
        "r": r_fixed,
        "sigma": sigma_fixed,
    }
    fixed_params[param] = st.slider(
        f"Adjust {param_labels[param]}",
        float(param_ranges[param][0]),
        float(param_ranges[param][-1]),
        float(fixed_params[param]),
    )
    fig = create_sensitivity_plot(param, param_ranges[param], fixed_params)
    st.plotly_chart(fig, use_container_width=True)
