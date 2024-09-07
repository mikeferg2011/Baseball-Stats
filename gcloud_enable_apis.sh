## declare an array variable
declare -a arr=("cloudresourcemanager.googleapis.com"
                "workflows.googleapis.com" 
                "bigquery.googleapis.com"
                "cloudfunctions.googleapis.com"
                "cloudbuild.googleapis.com"
                "secretmanager.googleapis.com"
               #  "run.googleapis.com"
                )

## now loop through the above array
for i in "${arr[@]}"
do
   echo "$i"
   gcloud services enable "$i"
done