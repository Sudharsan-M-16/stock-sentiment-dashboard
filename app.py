import streamlit as st
import yfinance as y
import datetime
import requests
import pandas as pd
import textblob
import matplotlib.pyplot as plt
from functions import get_stock_data,get_sentiment,highlight_sentiment
from dotenv import load_dotenv
import os
st.title("📈 Stock Sentiment Dashboard")
st.subheader("📈 Track Stock Prices & News Sentiments")
st.write("Welcome! Let's get this started.")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):")
st.markdown("ℹ️ Try tickers like `AAPL`, `GOOG`, `TSLA`, `MSFT` for better news coverage.")
start_date=st.date_input("Start Date",datetime.date.today())
end_date=st.date_input("End Date",start_date +datetime.timedelta(days=1))
if ticker:
    st.write(f"You selected: {ticker}")
    try:
        hist=get_stock_data(ticker,start_date,end_date)
        if hist.empty:
            st.warning("No data found enter a valid stock ticker")
        else:
            try:
                load_dotenv()
                api_key = os.getenv("NEWS_API_KEY")
                url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={api_key}"
                res=requests.get(url)
                articles=res.json()
                if not articles.get("articles"):
                    st.warning("No news articles found for this ticker".title())
                else:
                    headlines=[article["title"] for article in articles["articles"] if "title" in article][:5]
                    sentiments = [get_sentiment(headline)for headline in headlines]
                    df=pd.DataFrame({"Headlines":headlines,"Sentiments":sentiments})
                    df["Label"] = df["Sentiments"].apply(lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral"))
                    df1=df.style.applymap(highlight_sentiment, subset=["Label"])
                    st.write("   🧠 News Sentiment Analysis")
                    st.dataframe(df1)
                    label_counts = df["Label"].value_counts()
                    fig, ax = plt.subplots()
                    ax.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')
                    char_type=st.sidebar.selectbox("Choose Chart Type",["Bar Chart","Pie Chart"])
                    if char_type=="Bar Chart":
                        st.write("📊   Sentiment Breakdown(Bar Chart)")
                        st.bar_chart(label_counts)
                    else:
                        st.subheader("📊 Sentiment Distribution")
                        st.pyplot(fig)
                    df.to_csv("sentiment_output.csv", index=False)
                    st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name="sentiment_data.csv", mime="text/csv")

                        
            except Exception as r:
                st.error(f"ERROR!Something Went Wrong{r}")
            st.subheader(f"🕰️   Stock Price Data between the selected dates for {ticker}")
            st.line_chart(hist['Close'])
            hist["MA20"] = hist['Close'].rolling(window=20).mean()  # 20-day Moving Average
            st.subheader(f"📊 Moving Average (20-day) for {ticker}")
            st.line_chart(hist[["Close", "MA20"]])
            st.subheader(f"📦  The Stock Price and volume overview for {ticker}".title())
            st.line_chart(hist['Volume'])
            st.success("✅ Fetched data successfully!")
            st.markdown("---")
            st.success("✅ Built with ❤️ using Streamlit, yFinance, NewsAPI, and TextBlob.")

    except Exception as e:
        st.error(f"ERROR!Something went wrong {e}")
        
