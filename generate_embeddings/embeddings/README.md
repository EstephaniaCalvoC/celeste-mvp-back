# Tokenizer

Split the texts in each row to meet with the maximun tokens allowed in the used model.

## How to Use
To create the embeddings, you will need to follow these steps:

1. Open a command prompt and navigate to the cloned repository, and go inside embeddings directory.
1. Run the script with the following parameters:

	`./embeddings.py`

1. Check if the `embeddings.csv` in the Processed directory.


**Notes:**

- You can see [here](https://platform.openai.com/docs/models/) the maximun tokens allowed in the OpenAI models. Also have into account the [Rate Limits](https://platform.openai.com/account/rate-limits).

- Make sure you have set the following environment variables:
	- PROCESSED_TEXTS_DIRECTORY
	- IMAGES_PATH
	- ENGINE
	- MAX_TOKENS
	- OPENAI_API_KEY
