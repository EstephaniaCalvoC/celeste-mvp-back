# celeste-mvp-back
Celeste chat bot's backend

# Set up

**Note**: If you don't have a csv file with the embeddings, please follow the [generate embeddings guide](./generate_embeddings/README.md)

## Setup

To use the web crawler, you will need to follow these steps:

1. Clone the repository to your local machine.
1. Create a virtual environment
    ```bash
	python3.10 -m venv
    source venv/bin/activate
	```
1. Install setuptools

	```bash
	sudo apt-get install python3-setuptools
	pip install setuptools
	pip install --upgrade setuptools
	```
1. Install the required Python packages: `pip install -r requirements.txt`

1. Fill out the enviroment variables' values in the file: `.env.sh`

1. Set the enviroment variables: `source .env.sh`

# How to use

TODO:

1. Create Q/A system.
2. Add logs
3. Clean requirements for generate_embeddings
4. Improve doc strings
