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
                "roles/cloudfunctions.developer"
                "roles/cloudbuild.builds.editor"
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

gcloud builds triggers create github \
   --name="master-trigger" \
   --repo-name="Baseball-Stats" \
   --repo-owner="mikeferg2011" \
   --branch-pattern="^master$" \
   --build-config="cloudbuild.yaml" \
   --service-account="projects/baseball-434300/serviceAccounts/baseball-434300@appspot.gserviceaccount.com" \
   --require-approval \
   --include-logs-with-status