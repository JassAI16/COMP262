import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim.downloader as api
import random

# Load the dataset
jaspreet_df = pd.read_csv('C:/Users/jassn/Documents/Desktop/winter 2025/Natural Language & Recom Sys (SEC. 001)/assignments/Assignment 1/solution/COVID19_mini.csv')

# Drop the 'user' column if it exists
if 'user' in jaspreet_df.columns:
    jaspreet_df.drop('user', axis=1, inplace=True)

# Function to clean tweets
def clean_tweet(tweet):
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'\@w+', '', tweet)  # Removes @mentions
    tweet = re.sub(r'#', '', tweet)  # Removes hashtags
    tweet = re.sub(r'\d+', '', tweet)  # Removes numbers
    tweet = re.sub(r'[^\w\s]', '', tweet)  # Remove punctuations
    tweet = tweet.lower()
    tweet = re.sub(r'\s+', ' ', tweet).strip()
    return tweet

# Clean tweets
jaspreet_df['text'] = jaspreet_df['text'].apply(clean_tweet)

# Download the Word2Vec model
model = api.load('word2vec-google-news-300')

# Function to augment text
def augment_text(text):
    words = word_tokenize(text)
    words = [word for word in words if word in model.key_to_index]
    num_words_to_replace = min(3, len(words))
    
    for _ in range(num_words_to_replace):
        word_to_replace = random.choice(words)
        # Get the most similar word from the model
        similar_words = model.most_similar(word_to_replace, topn=10)
        new_word = random.choice(similar_words)[0]
        # Replace one occurrence of the word in the text
        words = [new_word if word == word_to_replace else word for word in words]
    
    return ' '.join(words)

# Apply augmentation
jaspreet_df['augmented_text'] = jaspreet_df['text'].apply(augment_text)
augmented_df = jaspreet_df.copy()
augmented_df['text'] = augmented_df['augmented_text']
augmented_df.drop('augmented_text', axis=1, inplace=True)

# Combine original and augmented data
final_df = pd.concat([jaspreet_df, augmented_df], ignore_index=True)
final_df.to_csv('C:/Users/jassn/Documents/Desktop/winter 2025/Natural Language & Recom Sys (SEC. 001)/assignments/Assignment 1/solution/jaspreet_df_after_random_insertion.csv', index=False)

print("Data preprocessing and augmentation completed. Check the jaspreet_df_after_random_insertion.csv file.")
