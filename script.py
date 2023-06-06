import cohere
import csv
import os
import time

from cohere.responses.classify import Example
from dotenv import load_dotenv

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

API_KEY = os.getenv("API_KEY")

co = cohere.Client(API_KEY)

# Training data
examples = [
    Example("you are hot trash", "Toxic"),
    Example("go to hell", "Toxic"),
    Example("get rekt moron", "Toxic"),
    Example("get a brain and use it", "Toxic"),
    Example("say what you mean, you jerk.", "Toxic"),
    Example("Are you really this stupid", "Toxic"),
    Example("I will honestly kill you", "Toxic"),
    Example("yo how are you", "Benign"),
    Example("I'm curious, how did that happen", "Benign"),
    Example("Try that again", "Benign"),
    Example("Hello everyone, excited to be here", "Benign"),
    Example("I think I saw it first", "Benign"),
    Example("That is an interesting point", "Benign"),
    Example("I love this", "Benign"),
    Example("We should try that sometime", "Benign"),
    Example("You should go for it", "Benign"),
]

# Get user input
url = input("Please provide the YouTube URL: ")
num_comments = 0
while num_comments <= 0 or num_comments > 96:
    num_comments = int(input("How many comments would you like to extract (max: 96): "))

print("Scraping comments... this should take around 10 seconds")

# Open the video in Chrome
with Chrome(service=Service(ChromeDriverManager().install())) as driver:
    wait = WebDriverWait(driver, 15)
    driver.get(url)

    # Scroll down in the page to make comments visible
    for item in range(20):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(
            Keys.END
        )
        time.sleep(0.25)

    # Scrape comments using the #context-text id attribute
    data = []
    for comment in wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))
    ):
        parsed_comment = " ".join(comment.text.split()).replace('"', "")
        data.append(parsed_comment)

# Use the Cohere API to retrieve predictions
response = co.classify(model="large", inputs=data[0:num_comments], examples=examples)

if os.path.exists("predictions.csv"):
    os.remove("predictions.csv")

print("Writing results to predictions.csv")

# Write the results to predictions.csv
with open("predictions.csv", "w", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(["comment", "prediction"])
    for comment, classification in zip(data, response.classifications):
        writer.writerow([comment, classification.prediction])

print("All done!")
