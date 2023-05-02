# Tokenizer

Split the texts in each row to meet with the maximun tokens allowed in the used model.

## How to Use
To use the tokenizer, you will need to follow these steps:

1. Open a command prompt and navigate to the cloned repository, and go inside embeddings directory.
1. Run the crawl.py script with the following parameters:

	`./tockenizer.py max_tokens`

	- max_tokens: Maximun amount of tokens allowed for the used model.
1. Create the embeddings


**Notes:**

- You can see the tokens distribution running: `./histogram_gen.py <<image_path>>`.

- You can see [here](https://platform.openai.com/docs/models/) the maximun tokens allowed in the OpenAI modells.






