# Detecting Toxic YouTube Comments using the Cohere API

A script used to scrape comments from specified YouTube videos and classify each comment as either "Toxic" or "Benign" using [Cohere's classification API endpoint](https://docs.cohere.com/reference/classify).

## Setup

1. Set up a Python virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Retrieve your Cohere API key (https://dashboard.cohere.ai/api-keys) and add it to a `.env` file in the project root directory

## Running the program

Run `script.py`. After specifying the YouTube video URL and the number of comments you want to extract, the comments and their predicted classifications (i.e. "Toxic" or "Benign") will be added to a `predictions.csv` file.
