# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import CREDENTIALS

def main():
    google_json = CREDENTIALS.GOOGLE_NLP_PATH
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_json

    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    text = u'Hello, world!'
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


if __name__ == "__main__":
    main()