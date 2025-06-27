import yfinance as y
import textblob
def get_stock_data(ticker, start, end):
    stock = y.Ticker(ticker)
    return stock.history(start=start, end=end)
def get_sentiment(text):
    return textblob.TextBlob(text).sentiment.polarity
def highlight_sentiment(val):
    color = ''
    if val == 'Positive':
        color = 'lightgreen'
    elif val == 'Negative':
        color = 'lightcoral'
    elif val == 'Neutral':
        color = 'lightgray'
    return f'background-color: {color}'