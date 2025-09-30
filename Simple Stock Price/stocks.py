import streamlit as st
import yfinance as yf
import altair as alt
import datetime

st.set_page_config(page_title="📈 Stock Price Viewer", layout = "wide")

st.markdown(
    "<h1 style='text-align: center; margin-top: -60px'>📈 Stock Price Viewer</h1>",
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 2])

with col1:
  popular_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Google": "GOOG",
    "NVIDIA": "NVDA",
    "Meta": "META"
  }
  ticker_buttons = st.columns(len(popular_tickers))

  input_ticker = st.radio(
    "🔥Popular Tickers",
    list(popular_tickers.keys()),
    horizontal=True
  )
  st.session_state["selected_ticker"] = popular_tickers[input_ticker]

  input_ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, TSLA)", value=st.session_state.get("selected_ticker", "AAPL"))

  input_start_date = datetime.date.today() - datetime.timedelta(days=30)
  input_end_date = datetime.date.today()

  input_start_date = st.date_input("Enter Start Date", value=input_start_date)
  input_end_date = st.date_input("Enter End Date", value=input_end_date)

  ticker = yf.Ticker(input_ticker)
  info = ticker.info
  st.subheader(f"{info['longName']}")
  st.markdown(f"**Sector**: {info['sector']}")
  st.markdown(f"**Industry**: {info['industry']}")
  st.markdown(f"**Market capitalization**: {info['marketCap']}")
  st.markdown(f"**Currency**: {info['currency']}")
  website = info.get("website", "N/A")
  if website != "N/A":
      st.markdown(f"**Website:** [***{website}***]({website})")
  else:
      st.write("**Website:** N/A")


with col2:
  if ticker:
      try:
          df = ticker.history(start=input_start_date, end=input_end_date)
          df.reset_index(inplace=True)

          st.subheader(f"Stock Data for {input_ticker} ({info['currency']})\nfrom {input_start_date} to {input_end_date}")

          df_melted = df.melt(id_vars=["Date"], value_vars=["Open", "Close"], var_name="Price Type", value_name="Price")

          price_chart = (
              alt.Chart(df_melted)
              .mark_line()
              .encode(
                  x="Date:T",
                  y=alt.Y("Price:Q", scale=alt.Scale(zero=False)),
                  color=alt.Color("Price Type:N", legend=alt.Legend(title=None,orient="top-right")),
                  tooltip=["Date:T", "Price Type:N", "Price:Q"]
              )
              .properties(title=f"{input_ticker} Open vs Close Prices")
          )

          volume_chart = (
              alt.Chart(df)
              .mark_line(color="orange")
              .encode(
                  x="Date:T", 
                  y=alt.Y("Volume:Q", axis=alt.Axis(format=".2s")),  # short SI format for large numbers
                  tooltip=["Date:T", "Volume:Q"]
              )
              .properties(title=f"{input_ticker} Volume (the total number of shares traded that day)")
          )
          st.altair_chart(price_chart, use_container_width=True)
          st.altair_chart(volume_chart, use_container_width=True)
      except Exception as e:
          st.error(f"Error fetching data: {e}")
  else:
      st.info("Please enter a stock ticker to get started.")

