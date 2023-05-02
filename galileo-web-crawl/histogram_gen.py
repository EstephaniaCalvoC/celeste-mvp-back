#!/usr/bin/env python3

import os
import pandas as pd
import tiktoken
import matplotlib
import sys


def create_histogram():
    """
    Crate a histogram to visualize the distribution of the number of tokens per row.
    Save the image in a given path.
    """
    image_path = sys.argv[1]
    
    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    df = pd.read_csv(os.getenv("PROCESSED_TEXTS_DIRECTORY"), index_col=0)
    df.columns = ['title', 'text']
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    hist = df.n_tokens.hist()
    matplotlib.pyplot.savefig(image_path)
 

def main():
    create_histogram()
 
 
if __name__ == "__main__":
    main()
