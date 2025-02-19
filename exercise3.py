import pandas as pd
import re
from sklearn.metrics import accuracy_score, f1_score

# Load the dataset
filename = 'COVID19_data.csv'  # Update this according to your name's initial
df = pd.read_csv(filename)

# Drop the 'user' column
df.drop('user', axis=1, inplace=True)

# Clean the tweets
def clean_tweet(tweet):
    tweet = re.sub(r'https?://\S+', '', tweet)  # Remove URLs
    tweet = re.sub(r'@\w+', '', tweet)  # Remove mentions
    tweet = re.sub(r'#\S+', '', tweet)  # Remove hashtags
    tweet = re.sub(r'\s+', ' ', tweet).strip()  # Remove extra spaces and trailing spaces
    return tweet

df['text'] = df['text'].apply(clean_tweet)

# Data exploration: Display basic information about the dataset
print(df.describe())
print(df.head())

# Add column for tweet length
df['tweet_len'] = df['text'].apply(len)

# Define positive and negative lexicons
positive_words = ['good', 'great', 'best', 'wonderful', 'happy', 'love', 'excellent', 'amazing', 'well', 'nice']
negative_words = ['bad', 'worst', 'terrible', 'awful', 'sad', 'hate', 'poor', 'horrible', 'negative', 'hard']

# Calculate sentiment
def calculate_sentiment(row):
    words = row['text'].lower().split()
    positive_hits = sum(1 for word in words if word in positive_words)
    negative_hits = sum(1 for word in words if word in negative_words)
    total_words = len(words)
    
    positive_percent = positive_hits / total_words if total_words > 0 else 0
    negative_percent = negative_hits / total_words if total_words > 0 else 0
    
    row['positive_percent'] = round(positive_percent, 2)
    row['negative_percent'] = round(negative_percent, 2)

    if positive_percent == negative_percent:
        return 'neutral'
    elif positive_percent > negative_percent:
        return 'positive'
    return 'negative'

df['predicted_sentiment_score'] = df.apply(calculate_sentiment, axis=1)

# Compare with original sentiments and calculate metrics
original_sentiments = df['sentiment']
predicted_sentiments = df['predicted_sentiment_score']

accuracy = accuracy_score(original_sentiments, predicted_sentiments)
f1 = f1_score(original_sentiments, predicted_sentiments, average='weighted', labels=['positive', 'negative', 'neutral'])

print(f"Accuracy: {accuracy}")
print(f"F1 Score: {f1}")

# Export the dataframe with new columns and scores
df.to_csv('updated_sentiment_analysis.csv', index=False)
