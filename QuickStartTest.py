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
    text = u' Knowledge of one or more of the following technologies is required: C, C++, C#, .NET, Java, Angular, Web Technologies, Xamarin, mobile technologies, design patterns, SQL, Database technologies, XML, Perl, Python, MatLab  Familiarity or interest in one or more of the following areas: Agile, Scrum, DevOps, Continuous Integration/Continuous Development (CI/CD) Pipeline, Version Control, TFS, Azure DevOps, GitHub, Product documentation, Process Documentation  Strong verbal/written communication skills  Prior work on projects in a team environment preferred  Relevant academic projects, internship or lab experience preferred '
    text = text.encode("ascii", "ignore")
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    encoding_type = enums.EncodingType.UTF8
    sentiment = client.analyze_entities(document=document, encoding_type=encoding_type)

    # Loop through entitites returned from the API
    for entity in sentiment.entities:
        print(u"Representative name for the entity: {}".format(entity.name))

        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))

        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))

        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))

            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(sentiment.language))
    print('Text: {}'.format(text))
    #print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


if __name__ == "__main__":
    main()