import os
import gzip
from datetime import datetime

def process_files(local_directory):
    for filename in os.listdir(local_directory):
        file_path = os.path.join(local_directory, filename)
        
        if filename.endswith('.log'):
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S')
            
            file_parts = filename.split('.')
            
            if file_parts[0] == "1234567": # Change to your desired prefix
                new_filename = f"{timestamp}.{'.'.join(file_parts[1:])}"
                new_file_path = os.path.join(local_directory, new_filename)
                
                with open(file_path, 'rb') as original_file:
                    with gzip.open(new_file_path + '.gz', 'wb') as gz_file:
                        gz_file.write(original_file.read())
                
                os.remove(file_path)
                
                print(f"Processed: {filename} -> {new_filename}.gz")

local_directory = 'Your/Dir/SubDir/'  # Change this to the directory where your .log files are located

if not os.path.exists(local_directory):
    os.makedirs(local_directory)

with open(os.path.join(local_directory, '1234567.Generated.Gibberish.access.log'), 'w') as f:
    f.write("Sample log content\n")

process_files(local_directory)