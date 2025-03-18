
# Testing The Function:

- To test the function in the Lambda Editor, insert your **bucket name** and **object key** to simulate an S3-triggered Lambda event.

- Sample Input:
```
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "<Your_Bucket_Name>"
        },
        "object": {
          "key": "1234567.Generated.Gibberish.access.log"
        }
      }
    }
  ]
}
```
  

- Sample Output:
```
{
"cloudwatchLogs": [
"Processing file: 1234567.Generated.Gibberish.access.log",
"Received file key from event: 1234567.Generated.Gibberish.access.log",
"Successfully compressed 1234567.Generated.Gibberish.access.log to 2023-07-15T10_15_00.Generated.Gibberish.access.log.gz"
],
"lambdaResponse": {
"statusCode": 200,
"body": "Processing complete."
},
"s3OutputFile": "2025-03-13T10_15_00.Generated.Gibberish.access.log.gz"
}
```
## Explanation:

### cloudwatchLogs:
A list of log messages that might be printed during processing.

### lambdaResponse:
The JSON response returned by the Lambda function.

### s3OutputFile:
The new file name stored in the S3 Bucket after processing it.
