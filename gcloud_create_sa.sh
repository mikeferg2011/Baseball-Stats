# create service account or use default service account like below
# gcloud iam service-accounts create
# baseball-434918@appspot.gserviceaccount.com
project_id="baseball-434918"
project_num="6919421047"

sa_name="baseball-prod"
sa_email="${sa_name}@${project_id}.iam.gserviceaccount.com"
echo $sa_name
echo $sa_email

gcloud iam service-accounts create $sa_name \
  --description="Service Account to run everything" \
  --display-name="Production Service Account"

gcloud iam service-accounts add-iam-policy-binding \
  $sa_name@$project_id.iam.gserviceaccount.com \
  --member="user:mikeferg2011@gmail.com" \
  --role="roles/iam.serviceAccountUser"


declare -a arr=("roles/editor"
                "roles/iam.serviceAccountUser"
                # "roles/workflows.editor"
                # "roles/logging.logWriter"
                "roles/bigquery.dataEditor"
                # "roles/bigquery.dataOwner"
                # "roles/bigquery.user"
                # "roles/bigquery.admin"
                # "roles/cloudfunctions.developer"
                # "roles/cloudfunctions.admin"
                # "roles/cloudbuild.builds.editor"
                # "roles/artifactregistry.reader"
                # "roles/artifactregistry.createOnPushRepoAdmin"
                # "roles/run.admin"
                
                )

for i in "${arr[@]}"
do
   echo "$i"
   gcloud projects add-iam-policy-binding $project_id \
      --member "serviceAccount:$sa_email" \
      --role "$i" \
      --condition=None
done


gcloud iam service-accounts keys create sa_key.json \
   --iam-account=$sa_email