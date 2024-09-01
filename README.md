# Baseball-Stats
Event Files From Retrosheet.org

Plan overview (8/31/2024)
- Create cloud database for hosting personal baseball database
- Create bigquery database
- load it with events from retrosheet and/or baseball reference
- use workflows to schedule automated refreshes
- Can use Cloud Run functions for on-demand compute to fetch data

Maybe make a graph database with neo4j to see what players played where, for what managers, won which awards
- https://cloud.google.com/blog/products/ai-machine-learning/analyze-graph-data-on-google-cloud-with-neo4j-and-vertex-ai
- there seems to be a free tier on gcp https://neo4j.com/pricing/#graph-database