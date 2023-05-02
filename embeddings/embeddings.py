#!/usr/bin/env python3

# TODO: Test

import os
import pandas as pd
import tiktoken
import matplotlib
import sys
import openai


def get_original_df():
    """
    Get data frame form the CSV file
    """
    
    df = pd.read_csv(os.getenv("PROCESSED_TEXTS_DIRECTORY" + "scraped.csv"), index_col=0)
    df.columns = ['title', 'text']
    
    return df

def create_histogram(df, image_path):
    """
    Crate a histogram to visualize the distribution of the number of tokens per row.
    Save the image in a given path.
    """
    
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    hist = df.n_tokens.hist()
    matplotlib.pyplot.savefig(image_path)
    
    
# Function to split the text into chunks of a maximum number of tokens
def split_into_many(text, tokenizer, max_tokens):

    # Split the text into sentences
    sentences = text.split('. ')
    
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    
    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater 
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of 
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks


def tokenizer(df, tokenizer, max_tokens):
    
    shortened = []
    
    # Loop through the dataframe
    for row in df.iterrows():
        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue
     
     	# If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'], tokenizer, max_tokens)
        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append(row[1]['text'] )
    
    return shortened



def create_embeddings(df):
    processed_path = os.getenv("PROCESSED_TEXTS_DIRECTORY")
    df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
    df.to_csv(processed_path + 'embeddings.csv')
    df.head()
 

def main():
    max_tokens = sys.argv[1]
    image_path = sys.argv[2]
    
    
    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    
    original_df = get_original_df()
    create_histogram(original_df, tokenizer, image_path + "_original")
    
    shortened = tokenizer(original_df, tokenizer, max_tokens)
    shortened_df = pd.DataFrame(shortened, columns = ['text'])
    
    create_histogram(shortened_df, image_path + "_shortened")
    
    create_embeddings(shortened_df)

 
 
if __name__ == "__main__":
    main()
