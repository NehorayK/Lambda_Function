import boto3
import gzip
import re
from io import BytesIO
from datetime import datetime

s3_client = boto3.client('s3')

def compress_log_file(bucket_name, file_key, regex_pattern):
    try:
        print(f"Processing file: {file_key}")

        if re.match(regex_pattern, file_key):
            response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = response['Body'].read()

            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S') # Using python3.13, 'datetime.utcnow()' Method will not work since it is been deprecated
                                                                        # Use 'datetime.now(datetime.timezone.utc)'
            file_parts = file_key.split('/')
            file_name = file_parts[-1]

            file_name_parts = file_name.split('.')

            if file_name_parts[0] == "1234567": # Insert Imperva Account_ID/Tenant_ID (Usually 7 Digits Associated With Your Cloud Environment)
                new_filename = f"{timestamp}.{'.'.join(file_name_parts[1:])}"
                new_file_key = '/'.join(file_parts[:-1]) + '/' + new_filename

                compressed_file = BytesIO()
                with gzip.GzipFile(fileobj=compressed_file, mode='wb') as gz_file:
                    gz_file.write(file_content)

                compressed_file.seek(0)

                s3_client.put_object(Bucket=bucket_name, Key=new_file_key + '.gz', Body=compressed_file)

                s3_client.delete_object(Bucket=bucket_name, Key=file_key)

                print(f"Successfully compressed {file_key} to {new_file_key}.gz")
                return {
                    'statusCode': 200,
                    'body': 'Processing complete.'
                }
            else:
                print(f"File {file_key} does not match the expected prefix, skipping.")
                return {
                    'statusCode': 200,
                    'body': 'File does not match the expected prefix, skipping.'
                }
        else:
            print(f"File {file_key} does not match the regex pattern, skipping.")
            return {
                'statusCode': 200,
                'body': 'File does not match the pattern, skipping.'
            }

    except Exception as e:
        print(f"Error processing file {file_key}: {e}")
        return {
            'statusCode': 500,
            'body': f"Error: {e}"
        }

def process_logs(bucket_name, regex_pattern):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name) # Listing the objects in the bucket to process the logs

        if 'Contents' in response:
            for obj in response['Contents']:
                file_key = obj['Key']
                if re.match(regex_pattern, file_key):
                    print(f"Processing file: {file_key}")
                    compress_log_file(bucket_name, file_key, regex_pattern)

        else:
            print("No files found in the bucket.")
        return {
            'statusCode': 200,
            'body': 'Logs processing complete.'
        }
    except Exception as e:
        print(f"Error listing objects in the bucket: {e}")
        return {
            'statusCode': 500,
            'body': f"Error: {e}"
        }

def lambda_handler(event, context):
    bucket_name = "<Your_Bucket_Name>" # Insert Your AWS S3 Bucket Name

    regex_pattern = r".*\.log$"

    if 'Records' in event:
        file_key = event['Records'][0]['s3']['object']['key'] # Slicing The Event Received In CloudWatch Once Log Being Uploaded To The Associated Bucket
        print(f"Received file key from event: {file_key}")
        return compress_log_file(bucket_name, file_key, regex_pattern)

    else:
        print("No event records found. Processing all .log files in the bucket.")
        return process_logs(bucket_name, regex_pattern)