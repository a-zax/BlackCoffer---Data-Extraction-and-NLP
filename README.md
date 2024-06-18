## BlackCoffer-Data-Extraction-NLP
The objective is to extract article text from provided URLs, clean and preprocess the text data, compute various textual analysis metrics, and then store the results in a structured format in an Excel file.

### Approach
#### 1.Data Extraction
Utilizes requests and BeautifulSoup libraries for web scraping to extract article text from URLs.
Extracted text includes only the article title and content, excluding headers, footers, and other non-article content.
Each article is saved as a separate text file named with its corresponding URL_ID.

#### 2.Text Analysis
Cleans the extracted text by removing punctuation, stopwords, and non-alphanumeric characters.
Computes several metrics including sentiment scores (positive and negative), polarity score, subjectivity score, average sentence length, percentage of complex words, fog index, average number of words per sentence, complex word count, word count, syllables per word, personal pronouns count, and average word length.
Uses NLTK and TextBlob libraries for tokenization, stopwords removal, sentiment analysis, and syllable counting.

#### 3.Output
Aggregates the computed metrics into a structured DataFrame.
Saves the output as an Excel file (Output Data Structure.xlsx) preserving the order and format as specified in the assignment.

#### 4.Dependencies
Requires Python 3.x with libraries such as requests, BeautifulSoup, pandas, nltk, and textblob.
Ensures all necessary NLTK resources (tokenizers, stopwords) are downloaded during script execution.

#### 5.Instructions
##### a)The file data_extraction.py & script (text_analysis.py) is designed to be run locally.
##### b)Before execution, ensure dependencies are installed (pip install -r requirements.txt).
##### c)Input data is provided in Input.xlsx, which contains URLs and corresponding URL_IDs.
##### d)Output is generated automatically as Output Data Structure.xlsx.
##### e) Detailed instructions on how to run the script and any setup requirements are provided in the README file.
