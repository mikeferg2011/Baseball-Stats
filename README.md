# Baseball-Stats
Event Files From Retrosheet.org

Plan overview (8/31/2024)
- Create cloud database for hosting personal baseball database
- Create bigquery database
- load it with events from retrosheet and/or baseball reference
- use workflows to schedule automated refreshes
- Can use Cloud Run functions for on-demand compute to fetch data
- Consider using Infrastructure as code approach. Terraform(?)

Maybe make a graph database with neo4j to see what players played where, for what managers, won which awards
- https://cloud.google.com/blog/products/ai-machine-learning/analyze-graph-data-on-google-cloud-with-neo4j-and-vertex-ai
- there seems to be a free tier on gcp https://neo4j.com/pricing/#graph-database

## GCP Details
- Project: Baseball
- Project ID: baseball-434300
- Guide to create and manage workflows [link](https://cloud.google.com/workflows/docs/creating-updating-workflow)


## Create local dev setup
```
python3 -m venv ./.venv
source ./.venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Initial Project setup steps
1. Create project
2. Enable APIs and set roles with `gcloud_api_commands.sh`
3. Create BigQuery dataset (schema) with `bigquery_setup.py`
4. Deploy workflow that runs python scripts to load data `some shell command`
   1. try to get this to run via CI/CD
5. 