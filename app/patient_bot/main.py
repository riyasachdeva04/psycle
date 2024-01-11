import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

# Define a global variable to store used quote IDs
used_quote_ids = set()

def load_quotes():
    with open("patient_bot/motivational_quotes.json", 'r') as file:
        data = json.load(file)
        # Assuming the key is "messages" in your JSON structure
        quotes_data = data.get("messages", [])
    return quotes_data

def get_most_apt_quote(user_input, quotes_data):
    global used_quote_ids  # Use the global variable

    # Analyze sentiment of the user input
    user_sentiment = TextBlob(user_input).sentiment.polarity

    # Extract quote texts and sentiments from the quotes_data
    quote_texts = [quote['text'] for quote in quotes_data]
    quote_sentiments = [TextBlob(quote_text).sentiment.polarity for quote_text in quote_texts]

    # Text Preprocessing (you can customize this based on your needs)
    quote_texts = [text.lower() for text in quote_texts]

    # Filter quotes with positive sentiment
    positive_quotes = [quote for quote, sentiment in zip(quotes_data, quote_sentiments) if sentiment > 0]

    # Exclude used quotes
    available_quotes = [quote for quote in positive_quotes if quote['id'] not in used_quote_ids]

    if not available_quotes:
        # If all quotes have been used, reset the used_quote_ids set
        used_quote_ids = set()
        available_quotes = positive_quotes

    # If the user input is negative, select a quote with positive sentiment
    if user_sentiment < 0 and available_quotes:
        most_apt_quote = max(available_quotes, key=lambda x: TextBlob(x['text']).sentiment.polarity)
    else:
        # If the user input is positive or neutral, use the original logic
        vectorizer = CountVectorizer().fit_transform(quote_texts)
        similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1])
        most_similar_index = similarities.argmax()
        most_apt_quote = available_quotes[most_similar_index]

    # Add the used quote ID to the set
    used_quote_ids.add(most_apt_quote['id'])

    return most_apt_quote
