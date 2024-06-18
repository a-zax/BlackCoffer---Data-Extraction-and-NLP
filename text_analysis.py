import string
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import re
from data_extraction import input_df

# Ensure nltk resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Load positive and negative word dictionaries
with open('MasterDictionary/positive-words.txt', 'r') as f:
    positive_words = set(f.read().split())
with open('MasterDictionary/negative-words.txt', 'r') as f:
    negative_words = set(f.read().split())

# Define stopwords list
stopwords_list = set(stopwords.words('english'))

# Additional stopwords from files
stopwords_files = [
    'stopwords/StopWords_Auditor.txt', 'stopwords/StopWords_Currencies.txt',
    'stopwords/StopWords_DatesandNumbers.txt', 'stopwords/StopWords_Generic.txt',
    'stopwords/StopWords_GenericLong.txt', 'stopwords/StopWords_Geographic.txt',
    'stopwords/StopWords_Names.txt'
]

for file in stopwords_files:
    with open(file, 'r') as f:
        stopwords_list.update(f.read().split())

def clean_text(text):
    # Remove punctuation and stopwords
    text = text.translate(str.maketrans('', '', string.punctuation))
    return ' '.join([word for word in text.split() if word.lower() not in stopwords_list])

def compute_variables(text):
    words = word_tokenize(text)
    cleaned_words = [word for word in words if word.isalnum() and word.lower() not in stopwords_list]

    positive_score = sum(1 for word in cleaned_words if word.lower() in positive_words)
    negative_score = sum(1 for word in cleaned_words if word.lower() in negative_words)

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)

    sentences = sent_tokenize(text)
    avg_sentence_length = len(cleaned_words) / len(sentences)

    complex_words = [word for word in cleaned_words if len(word) > 2]
    percentage_complex_words = len(complex_words) / len(cleaned_words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    avg_words_per_sentence = len(cleaned_words) / len(sentences)
    word_count = len(cleaned_words)
    syllable_count_per_word = sum([len(re.findall(r'[aeiouAEIOU]', word)) for word in cleaned_words]) / len(cleaned_words)
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in cleaned_words) / len(cleaned_words)

    return {
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sentence,
        "COMPLEX WORD COUNT": len(complex_words),
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": syllable_count_per_word,
        "PERSONAL PRONOUNS": personal_pronouns,
        "AVG WORD LENGTH": avg_word_length
    }

def analyze_text(text):
    blob = TextBlob(text)

    # Positive, Negative, Polarity, and Subjectivity scores
    positive_score = sum(1 for word in blob.words if TextBlob(word).sentiment.polarity > 0)
    negative_score = sum(1 for word in blob.words if TextBlob(word).sentiment.polarity < 0)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity

    # Additional metrics
    sentences = blob.sentences
    words = blob.words
    avg_sentence_length = sum(len(sentence.words) for sentence in sentences) / len(sentences)
    complex_word_count = sum(1 for word in words if len(TextBlob(word).syllables) >= 3)
    word_count = len(words)
    syllable_count_per_word = sum(len(TextBlob(word).syllables) for word in words) / word_count
    personal_pronouns = sum(1 for word in words if word.lower() in ['i', 'we', 'my', 'ours', 'us'])
    avg_word_length = sum(len(word) for word in words) / word_count

    return {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': polarity_score,
        'subjectivity_score': subjectivity_score,
        'avg_sentence_length': avg_sentence_length,
        'percentage_of_complex_words': complex_word_count / word_count * 100,
        'fog_index': 0.4 * (avg_sentence_length + complex_word_count / word_count * 100),
        'avg_number_of_words_per_sentence': avg_sentence_length,
        'complex_word_count': complex_word_count,
        'word_count': word_count,
        'syllable_per_word': syllable_count_per_word,
        'personal_pronouns': personal_pronouns,
        'avg_word_length': avg_word_length
    }

# Read extracted articles and perform analysis
output_data = []

for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    with open(f'{url_id}.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        cleaned_text = clean_text(text)
        variables = compute_variables(cleaned_text)
        variables['URL_ID'] = url_id
        variables['URL'] = row['URL']
        output_data.append(variables)

# Save output to Excel
output_df = pd.DataFrame(output_data)
output_df.to_excel('Output Data Structure.xlsx', index=False)
