
# yt-data

Data Engineering project using return youtube dislike API [RYD API](https://www.returnyoutubedislike.com)


## What this Project Does
Given a list of links to youtube channels, It collects the video id's of all videos by the youtube channel and gets the data required from RYD API endpoint. The data is then stored in GCS ,transformed using dbt and loaded into the data warehouse which is then used for Visualisations
### You can try adding channels of your own interest and seeing whether their content is `Decreasing in Quality` based upon the like to Dislike ratio

## Tools and technologies used
1. Selenium
2. Prefect
3. Google Cloud Platform(BigQuery and Google Cloud Storage)
4. dbt
5. Docker


## Steps To Recreate the Project

What you will need:
1. Docker[]
2. GCP or AWS or Azure account (create a service account with permissions for Bigquery and GCS )
3. [Prefect](https://www.prefect.io/)
4. dbt

1. Clone this repo
2. Build the docker image using the Dockerfile and push it to dockerhub
3. Configure prefect by adding cloud credentials of the service account and adding Docker block in the infrastructure,add the docker image you pushed instead of the default Prefect image.
4. Run python deploy.py to add the deployment to prefect (configure the deployment using cron jobs)
