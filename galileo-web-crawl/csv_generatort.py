#!/usr/bin/env python3
import os
from typing import List
import pandas as pd
from pandas.core.series import Series


def get_texts(texts_path: str) -> List:
    """
    Get a list of text files from a given directory and return the file names and their contents as a list of tuples.
    :param texts_path: The path to the directory containing the text files
    :return: A list of tuples containing the filename and the raw text from each file
    """
    texts=[]
    
    for file in os.listdir(texts_path + "/"):
        with open(texts_path + "/" + file, "r", encoding="UTF-8") as f:
            text = f.read()
            texts.append((file[len(texts_path):-4].replace('-',' ').replace('_', ' ').replace('#update',''), text))
    
    return texts


def remove_newlines(serie: Series) -> Series:
    """
    Remove newlines and extra spaces from a pandas Series object.
    :param serie: A pandas series containing strings with newlines
    :return: A pandas series with the newlines removed
    """
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


def create_csv_file(texts: List) -> None:
    """
    Create a CSV file from a list of text files.
    :param texts: A list of tuples containing the filename and the raw text from each file
    """
    
    df = pd.DataFrame(texts, columns = ['fname', 'text'])
    
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv(os.getenv("PROCESSED_TEXTS_DIRECTORY"))
    df.head()


def main():
    """
    The main function that runs the text processing script.
    """
    text_directory_path = os.getenv("TEXTS_PATH") + os.getenv("DOMINE")
    texts = get_texts(text_directory_path)
    create_csv_file(texts)
    

if __name__ == "__main__":
    main()
