# Web Crawler

This is a Python 3.9 web crawler that allows you to scrape the text from web pages within a specified domain.

## How to Use
To use the web crawler, you will need to follow these steps:

1. Open a command prompt and navigate to the cloned repository, and go inside web_crawl directory.
1. Run the crawl.py script with the following parameters:

	`./crawl.py full_url all_levels level`

	- full_url: the full URL of the starting page to crawl.
	- all_levels: whether to crawl all pages within the specified domain (1) or only the pages within the given level (0).
	- level: the maximum level of pages to crawl within the specified domain.

	The crawler will output the number of pages it is processing, and will save the text content of each page to a text file within the text/ directory.
1. Run the csv_generator.py script:
	`./csv_generator.py`
1. Check if the `craped.csv` file was created in the Processed directory.

**Note:**

- The crawler will skip pages that require JavaScript to run, and will not follow links to pages that contain the word "edit" or a "#" character in the URL.

- Make sure you have set the following environment variables:
	- PROCESSED_TEXTS_DIRECTORY
	- TEXTS_PATH
	- DOMINE
