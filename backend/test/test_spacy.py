import spacy
import trafilatura
from collections import Counter

# 1. Load the lightweight model (install with: python -m spacy download en_core_web_sm)
# nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_md")
# nlp = spacy.load("en_core_web_lg")
# nlp = spacy.load("en_core_web_trf")

def extract_tags(url):
    # Fetch content
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    
    # Process text through spaCy
    doc = nlp(text)
    
    # Extract specific entities
    # get top 10 Named Entity Recognition (NER) Tags
    # ner_tags = doc.ents
    # print all the entities with their labels
    # print([(tag.text, tag.label_) for tag in ner_tags])
    # ner_tags = sorted(ner_tags, key=lambda x: x.score, reverse=True)
    # ner_tags = ner_tags[:10]
    # return [{"text": tag.text, "label": tag.label_} for tag in ner_tags]

    # tags = {
    #     "persons": list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"])),
    #     "locations": list(set([ent.text for ent in doc.ents if ent.label_ == "GPE"])),
    #     "events": list(set([ent.text for ent in doc.ents if ent.label_ == "EVENT"])),
    #     "NER": list(set([ent.text for ent in doc.ents]))
    # }
    # return ner_tags
    # important_labels = ["PERSON", "GPE", "ORG", "EVENT"]
    
    # # Create a list of all detected entities that match our labels
    # tags = [ent.text for ent in doc.ents if ent.label_ in important_labels]
    
    # # Count occurrences and get the top 10
    # top_10 = Counter(tags).most_common(10)
    # print(top_10)
    # return top_10

    # Only keep tags that appear 2 or more times or appear in the first 1/3 of the text
    important_labels = ["PERSON", "GPE", "ORG", "EVENT"]
    tags = [ent.text for ent in doc.ents if ent.label_ in important_labels]
    tags = [tag for tag in tags if Counter(tags)[tag] >= 2 or tags.index(tag) < len(tags) / 2]
    # deduplicate tags
    tags = list(set(tags))

    print(tags)
    print(doc.text)
    print(doc.ents)
    return tags

if __name__ == "__main__":
    input_url = input("Enter the URL of the article: ")
    ner_tags = extract_tags(input_url)
    # for tag in ner_tags:
    #     print(tag["text"], tag["label"])