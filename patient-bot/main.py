import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

def load_quotes(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Assuming the key is "messages" in your JSON structure
            quotes_data = data.get("messages", [])
        return quotes_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{file_path}'. Check if the file is formatted correctly.")
        return None

def get_most_apt_quote(user_input, quotes_data):
    # Analyze sentiment of the user input
    user_sentiment = TextBlob(user_input).sentiment.polarity

    # Extract quote texts and sentiments from the quotes_data
    quote_texts = [quote['text'] for quote in quotes_data]
    quote_sentiments = [TextBlob(quote_text).sentiment.polarity for quote_text in quote_texts]

    # Text Preprocessing (you can customize this based on your needs)
    quote_texts = [text.lower() for text in quote_texts]

    # Filter quotes with positive sentiment
    positive_quotes = [quote for quote, sentiment in zip(quotes_data, quote_sentiments) if sentiment > 0]

    # If the user input is negative, select a quote with positive sentiment
    if user_sentiment < 0 and positive_quotes:
        most_apt_quote = max(positive_quotes, key=lambda x: TextBlob(x['text']).sentiment.polarity)
    else:
        # If the user input is positive or neutral, use the original logic
        vectorizer = CountVectorizer().fit_transform(quote_texts)
        similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1])
        most_similar_index = similarities.argmax()
        most_apt_quote = quotes_data[most_similar_index]

    return most_apt_quote

if __name__ == "__main__":
    # Path to the JSON file containing motivational quotes
    quotes_file_path = "motivational_quotes.json"

    # Load motivational quotes from the JSON file
    quotes_data = load_quotes(quotes_file_path)

    if quotes_data:
        # Get user input
        user_input = input("Enter your text: ")

        # Get the most apt quote based on user input and sentiment
        most_apt_quote = get_most_apt_quote(user_input, quotes_data)

        # Display the most apt quote
        print("\nMost Apt Quote:")
        print(f"ID: {most_apt_quote['id']}")
        print(f"Text: {most_apt_quote['text']}")
