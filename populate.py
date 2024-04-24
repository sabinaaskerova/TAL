import pandas as pd
import os

filename = os.getcwd()+'/data/train.tsv'
df = pd.read_csv(filename, sep='\t')
import requests

url = "http://localhost:8983/solr/african_french_press/update"

# Iterate over each row in the DataFrame and index it to Solr
for i in range(len(df)):
    data = {
        "add": {
            "doc": {
                "id" : i,
                "category": df.loc[i, "category"],
                "title": df.loc[i, "headline"],
                "content": df.loc[i, "text"]
            }
        }
    }
    response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    print(response.text)

# Commit the changes
response = requests.get(url + "?commit=true")
print(response.text)
