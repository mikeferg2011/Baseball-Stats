## declare an array variable
declare -a arr=("workflows.googleapis.com" 
                "bigquery.googleapis.com"
                "cloudfunctions.googleapis.com"
                "cloudbuild.googleapis.com"
                "secretmanager.googleapis.com"
                )

## now loop through the above array
for i in "${arr[@]}"
do
   echo "$i"
   gcloud services enable "$i"
done

# create service account or use default service account like below
# gcloud iam service-accounts create
# baseball-434300@appspot.gserviceaccount.com

declare -a arr=("roles/workflows.editor"
                "roles/logging.logWriter"
                "roles/bigquery.dataEditor"
                "roles/bigquery.dataOwner"
                "roles/bigquery.user"
                "roles/bigquery.admin"
                )

for i in "${arr[@]}"
do
   echo "$i"
   gcloud projects add-iam-policy-binding baseball-434300 \
        --member "serviceAccount:baseball-434300@appspot.gserviceaccount.com" \
        --role "$i"
#    gcloud services enable "$i"
done

gcloud iam service-accounts keys create sa_key.json \
    --iam-account=baseball-434300@appspot.gserviceaccount.com
# gcloud workflows deploy myFirstWorkflow --source=myFirstWorkflow.yaml \
#     --service-account=baseball-434300@appspot.gserviceaccount.com