from src.utils.yfinance_api import batch_query_stock_price
from src.utils.position import Position
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def find_pair_of_stocks():
    # Example list
    sp500_tickers = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "META",
        "TSLA",
        "JPM",
        "GS",
        "KO",
        "PEP",
    ]  # Example list

    stock_prices = batch_query_stock_price(sp500_tickers)

    price_df = pd.DataFrame(stock_prices)

    correlation_matrix = price_df.corr()

    # Step 4: Identify Most Correlated Pair
    correlated_pairs = correlation_matrix.unstack().sort_values(ascending=False)
    correlated_pairs = correlated_pairs[
        correlated_pairs < 1
    ]  # Remove self-correlations
    most_correlated_pair = correlated_pairs.idxmax()
    stock1, stock2 = most_correlated_pair

    return price_df[[stock1, stock2]], stock1, stock2


def compute_trading_signals(price_df: pd.DataFrame, stock1, stock2):

    # Step 5: Compute the Spread
    spread = price_df[stock1] - price_df[stock2]
    price_df["Spread"] = spread

    # Step 6: Compute Mean and Standard Deviation of the Spread
    rolling_window = 20
    price_df["Spread_Mean"] = spread.rolling(rolling_window).mean()
    price_df["Spread_Std"] = spread.rolling(rolling_window).std()
    price_df["Upper_Band"] = price_df["Spread_Mean"] + (2 * price_df["Spread_Std"])
    price_df["Lower_Band"] = price_df["Spread_Mean"] - (2 * price_df["Spread_Std"])

    # Step 7: Generate Trading Signals
    price_df["long_signal"] = price_df["Spread"] < price_df["Lower_Band"]
    price_df["short_signal"] = price_df["Spread"] > price_df["Upper_Band"]

    price_df["Long_Signal_value"] = np.where(
        price_df["long_signal"], price_df["Spread"], np.nan
    )
    price_df["Short_Signal_value"] = np.where(
        price_df["short_signal"], price_df["Spread"], np.nan
    )

    return price_df


def backtest_pair_trading():
    price_df, stock1, stock2 = find_pair_of_stocks()
    price_df = compute_trading_signals(price_df, stock1, stock2)
    print(price_df.iloc[0])
    available_cash = 1000
    initcash = available_cash
    positions = {}
    trigger = ""
    print("start")

    for idx, row in price_df.iterrows():
        if len(positions) == 0:
            if row["long_signal"]:
                print("Long signal on date:", row.name)
                trigger = "long"
                positions[stock1] = Position(
                    ticker=stock1,
                    entry_price=row[stock1],
                    side="long",
                    entry_date=row.name,
                    amount=available_cash // 2,
                )
                positions[stock2] = Position(
                    ticker=stock2,
                    entry_price=row[stock2],
                    side="short",
                    entry_date=row.name,
                    amount=available_cash // 2,
                )
        else:
            if trigger == "long" and row["Spread"] >= row["Spread_Mean"]:
                print("closing position on date:", row.name)
                long_pnl = positions[stock1].close_and_compute_pnl(
                    exit_price=row[stock1], exit_date=row.name
                )
                short_pnl = positions[stock2].close_and_compute_pnl(
                    exit_price=row[stock2], exit_date=row.name
                )

                print("long pnl", long_pnl)
                print("short pnl", short_pnl)
                total_pnl = long_pnl + short_pnl
                print("Total pnl of this trade", total_pnl)
                available_cash += total_pnl
                positions = {}
                trigger = None

            # if trigger == "short" and row["Spread"] <= row["Spread_Mean"]:
            #     # Close the short position
    print("Total cash after period", available_cash)
    rate = available_cash / initcash - 1
    print("Total rate of profit", rate * 100)


if __name__ == "__main__":
    backtest_pair_trading()


# # Step 8: Visualization with Plotly
# fig = go.Figure()

# # Plot Spread
# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Spread"],
#         mode="lines",
#         name="Spread",
#         line=dict(color="blue"),
#     )
# )

# # Plot Rolling Mean
# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Spread_Mean"],
#         mode="lines",
#         name="Mean",
#         line=dict(color="white", dash="dash"),
#     )
# )

# # Plot Upper and Lower Bands
# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Upper_Band"],
#         mode="lines",
#         name="Upper Band",
#         line=dict(color="red", dash="dot"),
#     )
# )
# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Lower_Band"],
#         mode="lines",
#         name="Lower Band",
#         line=dict(color="green", dash="dot"),
#     )
# )

# # Plot Buy (Long) Signals
# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Long_Signal"],
#         mode="markers",
#         name="Buy Signal",
#         marker=dict(color="green", size=8, symbol="triangle-up"),
#     )
# )

# # Plot Sell (Short) Signals
# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Short_Signal"],
#         mode="markers",
#         name="Sell Signal",
#         marker=dict(color="red", size=8, symbol="triangle-down"),
#     )
# )

# # Customize Layout
# fig.update_layout(
#     title=f"Pairs Trading: {stock1} vs {stock2}",
#     xaxis_title="Date",
#     yaxis_title="Price Spread",
#     template="plotly_dark",
# )

# # Show Plot
# # fig.show()


# fig_corr = go.Figure()

# # Create the heatmap with correlation numbers inside the squares
# fig_corr.add_trace(
#     go.Heatmap(
#         z=correlation_matrix.values,
#         x=correlation_matrix.columns,
#         y=correlation_matrix.index,
#         colorscale="RdBu",
#         colorbar=dict(title="Correlation"),
#         text=correlation_matrix.values,  # Use text to display the correlation values
#         texttemplate="%{text:.2f}",  # Format the text as correlation values with 2 decimals
#         hovertemplate="Correlation: %{text}<extra></extra>",  # Show value on hover
#         showscale=True,
#     )
# )

# fig_corr.update_layout(title="Stock Correlation Matrix")
# # fig_corr.show()


# initial_cash = 100000
# cash = initial_cash
# position = "flat"
# position_1 = 0  # shares of stock A
# position_2 = 0  # shares of stock B

# portfolio_values = []
# position_states = []

# for i in range(1, len(price_df)):
#     date = price_df.index[i]
#     spread = price_df["Spread"].iloc[i]
#     mean = price_df["Spread_Mean"].iloc[i]
#     lower = price_df["Lower_Band"].iloc[i]
#     upper = price_df["Upper_Band"].iloc[i]
#     price1 = price_df[stock1].iloc[i]
#     price2 = price_df[stock2].iloc[i]

#     # === ENTRY ===
#     if position == "flat":
#         if spread < lower:
#             # Long spread: Long stock1, Short stock2
#             position = "long_spread"
#             position_1 = cash / 2 / price1
#             position_2 = -cash / 2 / price2
#             cash = 0

#         elif spread > upper:
#             # Short spread: Short stock1, Long stock2
#             position = "short_spread"
#             position_1 = -cash / 2 / price1
#             position_2 = cash / 2 / price2
#             cash = 0

#     # === EXIT ===
#     elif position == "long_spread" and spread > mean:
#         # Exit long spread
#         cash = position_1 * price1 + position_2 * price2
#         position_1 = 0
#         position_2 = 0
#         position = "flat"

#     elif position == "short_spread" and spread < mean:
#         # Exit short spread
#         cash = position_1 * price1 + position_2 * price2
#         position_1 = 0
#         position_2 = 0
#         position = "flat"

#     # === Portfolio Value ===
#     portfolio_value = cash + position_1 * price1 + position_2 * price2
#     portfolio_values.append(portfolio_value)
#     position_states.append(position)

# # Add results to DataFrame
# price_df = price_df.iloc[1:]  # adjust for shifted results
# price_df["Portfolio_Value"] = portfolio_values
# price_df["Position"] = position_states
# price_df["Daily_Return"] = price_df["Portfolio_Value"].pct_change()

# from plotly.subplots import make_subplots

# # --- Create subplot: 2 rows
# fig = make_subplots(
#     rows=2,
#     cols=1,
#     shared_xaxes=True,
#     vertical_spacing=0.1,
#     subplot_titles=[
#         f"Spread & Trade Signals: {stock1} vs {stock2}",
#         "Backtested Portfolio Value",
#     ],
# )

# # --- Spread & Signals
# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Spread"],
#         mode="lines",
#         name="Spread",
#         line=dict(color="blue"),
#     ),
#     row=1,
#     col=1,
# )

# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Spread_Mean"],
#         mode="lines",
#         name="Mean",
#         line=dict(color="black", dash="dash"),
#     ),
#     row=1,
#     col=1,
# )

# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Upper_Band"],
#         mode="lines",
#         name="Upper Band",
#         line=dict(color="red", dash="dot"),
#     ),
#     row=1,
#     col=1,
# )

# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Lower_Band"],
#         mode="lines",
#         name="Lower Band",
#         line=dict(color="green", dash="dot"),
#     ),
#     row=1,
#     col=1,
# )

# # --- Entry/Exit Markers
# entry_long = (price_df["Position"].shift(1) == "flat") & (
#     price_df["Position"] == "long_spread"
# )
# entry_short = (price_df["Position"].shift(1) == "flat") & (
#     price_df["Position"] == "short_spread"
# )
# exit_trade = (price_df["Position"] != "flat") & (
#     price_df["Position"].shift(-1) == "flat"
# )

# fig.add_trace(
#     go.Scatter(
#         x=price_df.index[entry_long],
#         y=price_df["Spread"][entry_long],
#         mode="markers",
#         name="Enter Long Spread",
#         marker=dict(color="lime", symbol="triangle-up", size=10),
#     ),
#     row=1,
#     col=1,
# )

# fig.add_trace(
#     go.Scatter(
#         x=price_df.index[entry_short],
#         y=price_df["Spread"][entry_short],
#         mode="markers",
#         name="Enter Short Spread",
#         marker=dict(color="orange", symbol="triangle-down", size=10),
#     ),
#     row=1,
#     col=1,
# )

# fig.add_trace(
#     go.Scatter(
#         x=price_df.index[exit_trade],
#         y=price_df["Spread"][exit_trade],
#         mode="markers",
#         name="Exit Trade",
#         marker=dict(color="white", symbol="x", size=10),
#     ),
#     row=1,
#     col=1,
# )

# # --- Portfolio Value
# fig.add_trace(
#     go.Scatter(
#         x=price_df.index,
#         y=price_df["Portfolio_Value"],
#         mode="lines",
#         name="Portfolio Value",
#         line=dict(color="cyan"),
#     ),
#     row=2,
#     col=1,
# )

# # --- Layout
# fig.update_layout(
#     height=800,
#     template="plotly_dark",
#     showlegend=True,
#     title_text="Pairs Trading Strategy Backtest",
# )

# fig.update_xaxes(title_text="Date", row=2, col=1)
# fig.update_yaxes(title_text="Spread", row=1, col=1)
# fig.update_yaxes(title_text="Portfolio Value", row=2, col=1)

# fig.show()
