## Test Script Explanation

- This test script simulates the file manipulation process locally.
  
- It demonstrates how our mechanism:
  
	1. Identifies .log files in a specified directory.

	2. Renames files by prepending a UTC timestamp (formatted as YYYY-MM-DDTHH_MM_SS) to files that start with a specific prefix (here, "1234567").

	3. Compresses the renamed files into Gzip format (.gz).

	4. Deletes the original .log file after successful compression.

- How It Works?

1. Directory Listing:
The script uses os.listdir() to iterate over all files in the specified local directory.
2. File Filtering:
It processes only files that have a .log extension.
3. Timestamp Generation:
A timestamp is generated using datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S') (UTC time in ISO 9660-like format).
4. Filename Splitting & Prefix Check:
The filename is split by the dot (.) character. If the first part matches "1234567", the file is selected for processing.
5. New Filename Construction:
A new filename is built by prepending the timestamp to the remainder of the original filename.
6. Compression:
The script opens the original file in binary mode, compresses its contents with Gzip (creating a new file with a .gz extension), and writes the compressed data.
7. Cleanup:
After compression, the original .log file is deleted.
8. Logging:
Console messages are printed to show which file was processed and its new compressed name.

## Setup and Execution

1. Set the Directory
Update the local_directory variable with the path where your test .log files are located.
2. Create a Sample File
The script creates a sample file named 1234567.Generated.Gibberish.access.log in the directory with sample log content. This file is used to test the processing mechanism.
3. Run the Script
Execute the script using Python 3:
`
python3 script_name.py
`
4. Verify the Output:

• The console should display a message indicating the file was processed.
• The original .log file should be deleted.
• A new compressed file with a timestamped name (and a .gz extension) should appear in the same directory.

>Example input log:

	`1234567.Generated.Gibberish.access.log`

>Example output log (after the local script modification):

	`2025-03-13T10_15_00.Generated.Gibberish.access.log.gz`

## Summary

The test script verifies that our file manipulation process works correctly in a local environment.
It identifies `.log` files with a specific prefix, renames them with a timestamp, compresses them to Gzip format, and deletes the original files.
Use this script to ensure the process is functioning as expected before deploying it to a production environment.
