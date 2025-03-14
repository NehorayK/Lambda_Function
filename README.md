# AWS Lambda Log Compression And Rename 🚀📦

Welcome to the AWS Lambda Log Compression and rename project tailored for Incapsula!

This script automates the process of **compressing** and **renaming** log files stored in an S3 bucket. It’s designed to help you save storage space and manage your logs chronological order more efficiently while keeping things simple and precise for SIEM pulling the logs.

>  **Note:** Although this script is specifically designed for handling Incapsula log files (using a specific account/tenant ID prefix), you can easily modify it for other vendors by adjusting the **file prefix** check and **regex pattern**.

## Table of Contents 📑

- [How It Works ⚙️](#how-it-works-)

- [Features & Highlights ✨](#features--highlights-)

- [Setup & Usage 🚀](#setup--usage-)

- [Use Cases 🎯](#use-cases-)

- [Customization & Future Ideas 🔧](#customization--future-ideas-)

- [Welcome contributors 🤝](#Welcome-contributors-)

## How It Works ⚙️

1.  **Import & Setup**:

- Uses Python libraries such as **boto3** (AWS SDK) which sets up a connection with your S3 bucket , **gzip** for logs compression, **re** for regular expressions patterns, and **datetime** for timestamping and renaming each log for chronological order in the S3 Bucket.

2.  **Processing a Log File**:

-  **Validation**: Checks if the file name matches a specified regex pattern (default targets `.log` files).

-  **File Retrieval**: Your SIEM should be configured to actively fetch logs from your S3 Bucket using AWS S3 REST API Protocol.

-  **Timestamp Creation**: Generates a unique timestamp to rename the file. *(Note: a future update might replace `datetime.utcnow()` with `datetime.now(datetime.timezone.utc)` for better support.)*

-  **Vendor-Specific Prefix Check**: Verifies that the file name starts with a specific prefix, (e.g., `"1234567"` for Incapsula Cloud ID) if it does, the file being renamed with the current timestamp using python's timestamp library, for ISO 9660 format
`'%Y-%m-%dT%H_%M_%S'`.

>This step can be easily modified to suit log formats from other vendors.

-  **Compression & Update**: Compresses the file and uploads it back to S3 Bucket with a `.gz` extension, then deletes the original file (clean `.log.gz` files in the bucket)

>Example input log (being uploaded to the S3 Bucket):
	`1234567.Generated.Gibberish.access.log`

>Example output log (after the script modification in the S3 Bucket):
	`2025-03-13T10_15_00.Generated.Gibberish.access.log.gz`
  
4.  **Batch Processing**:

- If no specific file is provided via an event, the script can scan your entire bucket and process all matching log files.

5.  **Lambda Handler**:

- Acts as the main entry point.

- Determines if the Lambda is triggered by an S3 event or if it should process all log files.
  
- Returns informative status messages to help you keep track of operations.

## Features & Highlights ✨

-  **Easy S3 Integration**: Automatically interacts with your S3 bucket to fetch, compress, and update log files.

-  **Smart Filtering with Regex**: Processes only files that match your desired log format (e.g., `.log` files).

-  **Unique Timestamps**: Generates unique timestamps for each compressed file ensuring no two files clash.

-  **Efficient Compression**: Utilizes the power of `gz` to compress your logs quickly and efficiently.

-  **Vendor-Specific Safety Checks**: By default, the script verifies file names against a preset prefix (e.g., an Imperva Account/Tenant ID like `"1234567"`) to ensure that only the intended log files are processed.

-  **Error Handling & Feedback**: Provides clear messages and status codes to help you monitor what’s happening, right in your CloudWatch logs!

## Setup & Usage 🚀

1.  **AWS Lambda Configuration**:

- Create a new Lambda function in the AWS Management Console.

- Upload this script as your function code.

- Ensure your Lambda function has the necessary IAM permissions to interact with S3 (read, write, delete).

2.  **Update Your Settings**:

-  **Bucket Name**: Replace `<"Your_Bucket_Name">` with the name of your S3 bucket.

-  **Regex Pattern**: Adjust the regex `".*\.log$"` if you need to target different file types.

-  **Vendor Prefix**: Update the prefix check `"1234567"` in the script to match your Incapsula Account/Tenant ID.

>Modify the **prefix** if using the script for another vendor.

3.  **Triggering the Function**:

-  **Event-Based Trigger**: Configure your S3 bucket to invoke the Lambda when a new log file is uploaded.

-  **Manual Run**: You can also run the function manually to process all logs present in your bucket.

4.  **Monitoring & Troubleshooting**:

- Check AWS CloudWatch for logs to monitor the function’s execution.

- The script prints helpful messages to guide you through the process with indication of each rename and compression attempts.

## Use Cases 🎯

Here are some practical scenarios where this script can be highly beneficial:

-  **Real-Time Log Compression**:

When a new Incapsula log file is uploaded to your S3 bucket, the Lambda function is automatically triggered to compress the file. This ensures that logs are stored in a compressed format immediately, reducing storage space and improving efficiency.

-  **Batch Processing of Historical Logs**:

If you have accumulated a large number of log files over time, you can run the function manually to compress all existing `.log` files in your bucket. This is particularly useful during migration or maintenance windows.

-  **Cost Reduction & Storage Optimization**:

By compressing log files, you reduce the storage footprint on your S3 bucket, which can lead to lower storage costs and faster retrieval times when accessing logs for analysis.

-  **Vendor-Versitile Log Management**:

Specifically designed for Incapsula, but generally the script ensures that only logs starting with a specified 7 digits associated with your Incapsula cloud environment (which is regularly means your account/tenant ID).

The script look for those 7 digits in the file name, and replacing them with the current timestamp, to sort the logs chronological order in the bucket (required for the protocol in the SIEM for pulling the logs), and compressing each file that ends with `.log` using **gzip** python library (converting the end of the file to `.log.gz` format).

>With simple modifications, you can adapt it for logs from other vendors.

-  **Automated File Management Workflows**:

Integrate this Lambda function into your automated workflows to ensure that log files are consistently compressed and managed without manual intervention. This can be part of a larger automation or DevOps strategy.

-  **Enhanced Monitoring & Troubleshooting**:

With detailed logging provided by the script, you can monitor the processing of files via AWS CloudWatch, making it easier to track successes and identify any issues that arise during compression.

## Customization & Future Ideas 🔧

-  **Tailor the File Filter**: Change the regex and prefix conditions to suit different log formats or account identifiers that received in the log filename, and renaming it.

-  **Improve Timestamping**: Consider updating to the latest Python practices for UTC time management.

-  **Enhance Notifications**: Integrate AWS SNS to send alerts when files are processed or if errors occur.

-  **Expand Functionality**: Extend the script to handle other file types or add more advanced compression techniques.

## Welcome contributors 🤝

If you have suggestions, improvements, or bug fixes, feel free to fork the repository and open a pull request. Let’s collaborate and make this tool even better!
