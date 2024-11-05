import spacy
import csv
from collections import Counter
import matplotlib.pyplot as plt
from pypdf import PdfReader

nlp = spacy.load("en_core_web_sm")

def split_into_sentences(text):
    """
    Splits text into sentences
    IN: text, str, text to split into sentences
    OUT: sentences, list[str], sentences in the text
    """
    # join lines into a single paragraph
    text = text.replace("\n", " ")

    # remove leading and trailing whitespaces in the text
    """__Your_Code_Here__"""
    text = text.strip()
    # use spaCy to split the text into sentences
    """__Your_Code_Here__"""
    doc = nlp(text)
    sentences = [sentence.text for sentence in doc.sents]

    return sentences

def tokenize_sentence(sentence):
    """
    Tokenizes sentence into lemmatized words
    IN: sentence, str, sentence to tokenize
    OUT: tokenized_sentence, list[str], tokenized sentences
    """
    # use spaCy to tokenize the sentence into lemmatized words
    """__Your_Code_Here__"""
    doc = nlp(sentence)
    tokenized_sentence = [
    token.lemma_ 
    for token in doc 
    if not token.is_punct and not token.is_space
  ]
    return tokenized_sentence

def remove_stopwords(tokens):
    """
    Removes stopwords from tokens
    IN: tokens, list[str], tokens to remove stopwords from
    OUT: tokens, list[str], tokens with stopwords removed
    """
    # use spaCy to remove stopwords
    """__Your_Code_Here__"""

    tokens = [token for token in tokens if not nlp.vocab[token].is_stop]
    return tokens


def update_word_frequency(processed_text, cumulated_frequency=None):
    """
    Updates the cumulated word frequency with the frequency in the processed text
    IN: processed_text, list[list[str]], processed text to count word frequency
        cumulated_frequency, dict{str: int}, cumulated word frequency
    OUT: cumulated_frequency, dict{str: int}, cumulated word frequency
    """
    # if cumulated_frequency is not provided, initialize it
    """__Your_Code_Here__"""
    if cumulated_frequency == None:
        cumulated_frequency = Counter()
    else:
        cumulated_frequency = Counter(cumulated_frequency)


    # update the cumulated frequency with the frequency in each sentence
    """__Your_Code_Here__"""
    processed_text = [sentence.split() for sentence in processed_text]
    cumulated_frequency.update(word for sentence in processed_text for word in sentence)  # Combined update

    return cumulated_frequency


def plot_word_frequency_dist(cumulated_frequency):
    """
    Plots word frequency
    IN: cumulated_frequency, dict{str: int}, cumulated word frequency
    OUT: None
    """
    # plot the word frequency distribution
    """__Your_Code_Here__"""
    values = cumulated_frequency.values()
    plt.figure(figsize=(15,5))
    plt.hist(values)
    plt.xlabel("Word Frequency")
    plt.ylabel("Num of Words")
    plt.title("Word Frequency Distribution")
    plt.show()

def sort_words_by_frequency(cumulated_frequency):
    """
    Sorts words by frequency
    IN: cumulated_frequency, dict{str: int}, cumulated word frequency
    OUT: sorted_word_frequencies, list[tuple(str, int)], sorted words by frequency
    """
    # sort the words by frequency, breaking ties by word alphabetical order
    """__Your_Code_Here__"""
    sorted_words = sorted(cumulated_frequency.items(), key=lambda x: (-x[1], x[0]))
    return sorted_words


def find_mean_and_std(sorted_word_frequencies):
    """
    Finds mean and standard deviation of word frequency
    IN: sorted_word_frequencies, list[tuple(str, int)], sorted words by frequency
    OUT: mean, float, mean of word frequency
         std, float, standard deviation of word frequency
    """
    # access all the frequencies
    """__Your_Code_Here__"""
    frequencies = [frequency for _, frequency in sorted_word_frequencies]

    # calculate the mean
    """__Your_Code_Here__"""
    mean = sum(frequencies)/len(frequencies)

    # calculate the standard deviation
    """__Your_Code_Here__"""
    variance = sum((frequency - mean)**2 for frequency in frequencies) / len(frequencies)
    std = variance**.5
    return mean, std

import math

def bucket_value_by_mean_std(value, mean, std):
    """
    Buckets value by mean and standard deviation
    IN: value, int | float, value from a distribution to bucket
        mean, float, mean of the distribution
        std, float, standard deviation of the distribution
    OUT: bucket_idx, int, bucket index
    """
    # calculate the bucket index
    """__Your_Code_Here__"""
    bucket_val = (value-mean)/std
    bucket_idx = math.floor(bucket_val)
    
    return bucket_idx




def extract_pdf_text(file_path):
    """
    Extracts text from a PDF file as a string
    IN: file_path, str, path to the PDF file
    OUT: text, str, extracted text from all pages joined together with whitespaces
    """
    # create a reader to read the PDF file
    reader = PdfReader(file_path)

    text_list = [] # list to collect text from each page
    for page in reader.pages:
        # extract text from the page
        page_text = page.extract_text() 
        # append the text to the list
        text_list.append(page_text)

    # join the text from all pages with whitespaces
    text = ' '.join(text_list)
    return text


texts = "This is a sentence okay, but it shouldn't be. So ,amy words in this sentence. this is tiring to read the sentence"
tokens = tokenize_sentence(texts)
print(tokens)
frequency_tokens = update_word_frequency(tokens)
print(frequency_tokens)
frequency_sorted = sort_words_by_frequency(frequency_tokens)
print(frequency_sorted)
frequencies = [frequency for _, frequency in frequency_sorted]
print(find_mean_and_std(frequency_sorted))
mean_val, std_val = find_mean_and_std(frequency_sorted)
bucket_indexes = [bucket_value_by_mean_std(i, mean_val, std_val) for i in frequencies]
print(bucket_indexes)