import streamlit as st
import yfinance as yf
import pandas as pd

# Create a multi-page app
st.set_page_config(page_title="Financial Dashboard", page_icon=":chart:", layout="wide")

# Add a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Commodities", "ETFs", "Underpriced Stocks", "Cryptocurrencies", "Financial Statement Analysis", "Portfolio Builder"])

# Commodities page
if page == "Commodities":
    st.title("Commodities")
    commodity_tickers = ["GC=F", "CL=F", "NG=F"]
    commodity_names = ["Gold", "Crude Oil", "Natural Gas"]
    start_date = st.date_input("Enter start date")
    end_date = st.date_input("Enter end date")
    for ticker, name in zip(commodity_tickers, commodity_names):
        @st.cache_data(ttl=3600)  # Cache for 1 hour
        def download_data(ticker, start_date, end_date):
            return yf.download(ticker, start=start_date, end=end_date)
        data = download_data(ticker, start_date, end_date)
        st.write(f"{name} Chart")
        st.line_chart(data["Close"])

# ETFs page
elif page == "ETFs":
    st.title("ETFs")
    etf_tickers = ["SPY", "QQQ", "DIA"]
    etf_names = ["S&P 500", "Nasdaq-100", "Dow Jones"]
    start_date = st.date_input("Enter start date")
    end_date = st.date_input("Enter end date")
    for ticker, name in zip(etf_tickers, etf_names):
        @st.cache_data(ttl=3600)  # Cache for 1 hour
        def download_data(ticker, start_date, end_date):
            return yf.download(ticker, start=start_date, end=end_date)
        data = download_data(ticker, start_date, end_date)
        st.write(f"{name} Chart")
        st.line_chart(data["Close"])

# Underpriced Stocks page
elif page == "Underpriced Stocks":
    st.title("Underpriced Stocks Checker")
    ticker = st.text_input("Enter the stock ticker: ")
    if st.button("Get Data"):
        try:
            @st.cache_data(ttl=3600)  # Cache for 1 hour
            def download_data(ticker, start_date, end_date):
                return yf.download(ticker, start=start_date, end=end_date)
            start_date = "2020-01-01"
            end_date = "2022-02-26"
            data = download_data(ticker, start_date, end_date)
            data['MA50'] = data['Close'].rolling(window=50).mean()
            data['MA200'] = data['Close'].rolling(window=200).mean()
            if data['Close'].iloc[-1] < data['MA50'].iloc[-1] and data['Close'].iloc[-1] < data['MA200'].iloc[-1]:
                st.write(f"The stock {ticker} is underpriced.")
            else:
                st.write(f"The stock {ticker} is not underpriced.")
            st.write(data)
        except Exception as e:
            st.write(f"An error occurred: {e}")

# Cryptocurrencies page
elif page == "Cryptocurrencies":
    st.title("Cryptocurrencies")
    crypto_tickers = ["BTC-USD", "ETH-USD"]
    crypto_names = ["Bitcoin", "Ethereum"]
    start_date = st.date_input("Enter start date")
    end_date = st.date_input("Enter end date")
    for ticker, name in zip(crypto_tickers, crypto_names):
        @st.cache_data(ttl=3600)  # Cache for 1 hour
        def download_data(ticker, start_date, end_date):
            return yf.download(ticker, start=start_date, end=end_date)
        data = download_data(ticker, start_date, end_date)
        st.write(f"{name} Chart")
        st.line_chart(data["Close"])

# Financial Statement Analysis page
elif page == "Financial Statement Analysis":
    st.title("Financial Statement Analysis")
    ticker_input = st.text_input("Enter a ticker symbol")
    start_date = st.date_input("Enter start date")
    end_date = st.date_input("Enter end date")
    if ticker_input:
        ticker = yf.Ticker(ticker_input)
        st.write("Balance Sheet")
        st.write(ticker.balance_sheet)
        st.write("Income Statement")
        st.write(ticker.financials)
        st.write("Cash Flow Statement")
        st.write(ticker.cashflow)

# Portfolio Builder page
elif page == "Portfolio Builder":
    st.title("Portfolio Builder")
    stocks = []
    for i in range(5):  # Allow users to input up to 5 stocks
        stock_input = st.text_input(f"Enter stock {i+1} ticker symbol")
        if stock_input:
            stocks.append(stock_input)
    start_date = st.date_input("Enter start date")
    end_date = st.date_input("Enter end date")
    if stocks:
        portfolio_value = 0
        for stock in stocks:
            data = yf.download(stock, start=start_date, end=end_date)
            portfolio_value += data["Close"][-1]  # Add the current price of each stock to the portfolio value
        st.write(f"Portfolio value: ${portfolio_value:.2f}")

if __name__ == "__main__":
    st.write("Financial Dashboard")