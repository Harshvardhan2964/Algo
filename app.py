import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import time

# Set page configuration and title
st.set_page_config(
    page_title="Project Disha",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Custom CSS styles
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background: black; /* Change background color to black */
        color: white;
    }
    .stButton > button {
        background-color: #FF6600 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Define page title and header image
st.title("Algo")
image = Image.open("main1.jpg")  # Replace with your exhibition image
st.image(image, use_column_width=True)

# Sidebar for user input
st.sidebar.header('User Input')

# Create a link to Zerodha
zerodha_link = "https://zerodha.com"  # Replace with the actual Zerodha URL
st.sidebar.markdown(f"[Zerodha]({zerodha_link})")

# Add a "Trade now" button
if st.sidebar.button("Trade now"):
    st.sidebar.markdown(f"[Trade Now]({zerodha_link})")

# Option to select what to view
view_option = st.sidebar.radio("Select What to View", ["Nifty Bank Chart", "Nifty 50 Chart", "Data Table"])

def get_input():
    start_date = st.sidebar.text_input("Start Date", "2020-01-02")
    end_date = st.sidebar.text_input("End Date", "2023-01-02")
    return start_date, end_date

start_date, end_date = get_input()

st.sidebar.write(f"Selected Date Range: {start_date} to {end_date}")

# Function to fetch stock data
def fetch_stock_data():
    nifty_bank = '^NSEBANK'
    nifty_50 = '^NSEI'  # Nifty 50
    start_date = '2021-01-01'
    end_date = '2023-08-24'
    nb_data = yf.download(nifty_bank, start=start_date, end=end_date)
    nifty_50_data = yf.download(nifty_50, start=start_date, end=end_date)
    return nb_data, nifty_50_data  # Return as separate variables

# Check if the data is fetched successfully
try:
    nb_data, nifty_50_data = fetch_stock_data()  # Unpack the tuple
    st.success("Stock data fetched successfully.")
except Exception as e:
    st.error(f"Error fetching stock data: {str(e)}")
    nb_data = None
    nifty_50_data = None

# Function to determine market direction
def determine_market_direction(data):
    sma_9 = data['Close'].rolling(window=9).mean()
    sma_15 = data['Close'].rolling(window=15).mean()
    sma_20 = data['Close'].rolling(window=20).mean()

    if sma_9.iloc[-1] > sma_15.iloc[-1] > sma_20.iloc[-1]:
        return "Buy long"  # All SMAs are up
    elif sma_9.iloc[-1] < sma_15.iloc[-1] < sma_20.iloc[-1]:
        return "Short the market"  # All SMAs are down
    else:
        return "Sideways market"  # SMAs are crossing each other

# Determine market direction for Nifty Bank
if nb_data is not None:
    market_direction_nb = determine_market_direction(nb_data)

# Determine market direction for Nifty 50
if nifty_50_data is not None:
    market_direction_nifty_50 = determine_market_direction(nifty_50_data)

# Main content container
main_container = st.container()

# Main content
with main_container:
    if view_option == "Nifty Bank Chart" and nb_data is not None:
        # Create candlestick chart with moving averages
        sma_window = [9, 15, 20]

        for window in sma_window:
            nb_data[f'SMA_{window}'] = nb_data['Close'].rolling(window=window).mean()

        candlestick_fig = go.Figure()

        candlestick_fig.add_trace(go.Candlestick(
            x=nb_data.index,
            low=nb_data['Low'],
            high=nb_data['High'],
            close=nb_data['Close'],
            open=nb_data['Open'],
            increasing_line_color='green',
            decreasing_line_color='red'
        ))

        for window in sma_window:
            sma_trace = go.Scatter(
                x=nb_data.index,
                y=nb_data[f'SMA_{window}'],
                mode='lines',
                line=dict(width=2),
                name=f'SMA {window}'
            )
            candlestick_fig.add_trace(sma_trace)

        candlestick_fig.update_layout(
            title='BANK NIFTY Spot Price with Simple Moving Averages',
            yaxis_title='Spot Price',
            xaxis_title='Date',
            legend=dict(x=0, y=1)
        )

        # Display the candlestick chart
        st.plotly_chart(candlestick_fig)

    elif view_option == "Nifty 50 Chart" and nifty_50_data is not None:
        # Create candlestick chart with moving averages
        sma_window = [9, 15, 20]

        for window in sma_window:
            nifty_50_data[f'SMA_{window}'] = nifty_50_data['Close'].rolling(window=window).mean()

        candlestick_fig = go.Figure()

        candlestick_fig.add_trace(go.Candlestick(
            x=nifty_50_data.index,
            low=nifty_50_data['Low'],
            high=nifty_50_data['High'],
            close=nifty_50_data['Close'],
            open=nifty_50_data['Open'],
            increasing_line_color='green',
            decreasing_line_color='red'
        ))

        for window in sma_window:
            sma_trace = go.Scatter(
                x=nifty_50_data.index,
                y=nifty_50_data[f'SMA_{window}'],
                mode='lines',
                line=dict(width=2),
                name=f'SMA {window}'
            )
            candlestick_fig.add_trace(sma_trace)

        candlestick_fig.update_layout(
            title='NIFTY 50 Spot Price with Simple Moving Averages',
            yaxis_title='Spot Price',
            xaxis_title='Date',
            legend=dict(x=0, y=1)
        )

        # Display the candlestick chart
        st.plotly_chart(candlestick_fig)

    elif view_option == "Data Table":
        if nb_data is not None:
            st.header("Nifty Bank Data")
            st.write(nb_data)

        if nifty_50_data is not None:
            st.header("Nifty 50 Data")
            st.write(nifty_50_data)

# Market Direction Section
if nb_data is not None or nifty_50_data is not None:
    st.markdown("<h2 style='padding-top: 20px; background-color: lightgreen;'>Market Direction</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    if view_option == "Nifty Bank Chart" and nb_data is not None:
        st.markdown(f"<h3>Nifty Bank: {market_direction_nb}</h3>", unsafe_allow_html=True)
    
    if view_option == "Nifty 50 Chart" and nifty_50_data is not None:
        st.markdown(f"<h3>Nifty 50: {market_direction_nifty_50}</h3>", unsafe_allow_html=True)
