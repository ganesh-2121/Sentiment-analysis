import pandas as pd
import tkinter as tk
from tkinter import messagebox
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data files (only if not already downloaded)
nltk.download('vader_lexicon')
nltk.download('punkt')

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Load abusive words from a CSV file
def load_abusive_words(file_path):
    try:
        df = pd.read_csv('train.csv')
        # Assuming the abusive words are in a column named "words"
        abusive_words = set(df['Abusive'].str.lower().dropna().tolist())
        return abusive_words
    except FileNotFoundError:
        messagebox.showerror("Error", "Abusive words file not found.")
        return set()
    except KeyError:
        messagebox.showerror("Error", "Column 'words' not found in the CSV file.")
        return set()

# Check if the comment contains any abusive language
def contains_abusive_language(comment, abusive_words):
    tokens = word_tokenize(comment.lower())
    for word in tokens:
        if word in abusive_words:
            return True
    return False

# Perform sentiment analysis using VADER
def analyze_sentiment(comment):
    sentiment_scores = sia.polarity_scores(comment)
    if sentiment_scores['compound'] >= 0.05:
        return "Positive comment"
    elif sentiment_scores['compound'] <= -0.05:
        return "Negative comment"
    else:
        return "Neutral comment"

# Handle comment submission in GUI
def submit_comment():
    comment = comment_entry.get()
    abusive_words = load_abusive_words("abusive_words.csv")  # Load abusive words file

    if contains_abusive_language(comment, abusive_words):
        messagebox.showerror("Abusive Comment", "The comment you typed contains abusive language and cannot be allowed.")
    else:
        vader_result = analyze_sentiment(comment)
        messagebox.showinfo("Sentiment Analysis Result", f"Comment sentiment: {vader_result}")

# Create the tkinter GUI window
root = tk.Tk()
root.title("Comment Sentiment and Abusive Check")
root.geometry("400x200")

# Label and entry for the comment
comment_label = tk.Label(root, text="Enter your comment:")
comment_label.pack(pady=10)

comment_entry = tk.Entry(root, width=50)
comment_entry.pack(pady=10)
    
# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_comment)
submit_button.pack(pady=10)

# Run the GUI main loop
root.mainloop()
