import pandas as pd
import os
import requests
import spacy

filename = os.getcwd()+'/data/train.tsv'
df = pd.read_csv(filename, sep='\t')
url = "http://localhost:8983/solr/african_french_press/update"

nlp = spacy.load("fr_core_news_sm")

# fr_core_news_sm has three NER labels only: LOC, PER, and ORG (+MISC)
def extract_entities(text):
    doc = nlp(text)
    entities = {
        "location": set(),
        "person": set(),
        "organization": set()
    }
    for ent in doc.ents:
        if ent.label_ == "LOC":
            entities["location"].add(ent.text)
        elif ent.label_ == "PER":
            entities["person"].add(ent.text)
        elif ent.label_ == "ORG":
            entities["organization"].add(ent.text)
    return entities



for i, row in df.iterrows():
    entities = extract_entities(row['text'])
    
    article_entities = {
        "id": i,
        "category": row["category"],
        "title": row["headline"],
        "description": row["text"],
        "url": row["url"]
    }
    
    for entity_type, entity_set in entities.items():
        article_entities[f"enti_{entity_type}"] = list(entity_set)
    
    response = requests.post(url, json={"add": {"doc": article_entities}}, headers={"Content-Type": "application/json"})
    print(response.text)

response = requests.get(url + "?commit=true")
print(response.text)
