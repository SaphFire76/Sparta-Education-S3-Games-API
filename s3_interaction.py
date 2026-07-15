import json
import boto3
import os
from dotenv import load_dotenv



def save_to_s3(games):

    load_dotenv()

    bucket_name = "se-zain-testbucket"

    s3 = boto3.client("s3")

    # Save the games locally as JSON
    filename = "games.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(games, file, indent=4)

    # Upload to S3
    s3.upload_file(
        filename,
        bucket_name,
        filename
    )

    print(f"{filename} uploaded successfully.")



def fetch_from_s3():
    s3 = boto3.client("s3")

    bucket_name = "se-zain-testbucket"
    file_name = "games.json"

    response = s3.get_object(
        Bucket=bucket_name,
        Key=file_name
    )

    content = response["Body"].read().decode("utf-8")

    print(content)
