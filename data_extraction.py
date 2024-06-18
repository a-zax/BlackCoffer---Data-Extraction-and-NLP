import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the URLs from the input Excel file
input_df = pd.read_excel('Input.xlsx')

# Function to extract article text
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Assuming the title is in <h1> tag and article text in <p> tags
    title = soup.find('h1').get_text() if soup.find('h1') else ''
    paragraphs = soup.find_all('p')
    article_text = ' '.join([para.get_text() for para in paragraphs])

    return title, article_text

# Extract and save articles
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    title, article_text = extract_article_text(url)

    with open(f'{url_id}.txt', 'w', encoding='utf-8') as file:
        file.write(f'{title}\n{article_text}')
