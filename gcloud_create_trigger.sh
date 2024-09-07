project_id="baseball-434918"
project_num="6919421047"

sa_name="baseball-prod"
sa_email="${sa_name}@${project_id}.iam.gserviceaccount.com"

gcloud builds triggers create github \
   --region=us-central1 \
   --name="master-trigger" \
   --repo-name="Baseball-Stats" \
   --repo-owner="mikeferg2011" \
   --branch-pattern="^master$" \
   --build-config="cloudbuild.yaml" \
   --service-account="projects/$project_id/serviceAccounts/$sa_email" \
   --require-approval \
   --include-logs-with-status