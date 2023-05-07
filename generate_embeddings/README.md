# Generate Embeddings 

## Setup

To use the web crawler, you will need to follow these steps:

1. Clone the repository to your local machine.
1. Create a virtual environment
    ```bash
	python3.10 -m venv
    source venv/bin/activate
	```
1. Go to generate_embeddings directory
1. Install setuptools

	```bash
	sudo apt-get install python3-setuptools
	pip install setuptools
	pip install --upgrade setuptools
	```
1. Install the required Python packages: `pip install -r requirements.txt`

1. Fill out the enviroment variables' values in the file: `.env.sh`

1. Set the enviroment variables: `source .env.sh`


## How to Use

1. [Crawl the website](./galileo-web-crawl/README.md)
1. [Get the embeddings](./embeddings/README.md)
