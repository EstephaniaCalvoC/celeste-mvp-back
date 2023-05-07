###### Mandatory ######

# Website's domine
export DOMINE="your_website.com"

# Path to save the files with the pages' texts.
export TEXTS_PATH="/abs/celeste-mvp-back/text/"

# Path to save the CSV file with the pages' texts
export PROCESSED_TEXTS_DIRECTORY="/abs/celeste-mvp-back/processed/"

# Images path
export IMAGES_PATH="/abs/celeste-mvp-back/histogram"

# Model info

export ENGINE="text-embedding-ada-002"

export MAX_TOKENS=500

# OpenAI API key

export OPENAI_API_KEY=""



###### Optional ######

# URL of website to be processed
export WEB_SITE_URL="https://your_website.com/wiki"

# Use '1' to get all hyperlinks under the domain or '0' if to get the links up to the specified level. 
export READ_ALL_LINKS="0"

# Level for searching the links
export LEVEL="3"