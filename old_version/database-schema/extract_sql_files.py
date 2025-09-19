import os
import glob
import shutil

# Purpose: To extract sql objects to upload to Claude project knowledge. no other use.

def extract_sql_files():
    # Create the _extract directory if it doesn't exist
    if not os.path.exists("_extract"):
        os.makedirs("_extract")
    
    # Find all .sql files under the src directory
    sql_files = glob.glob("src/**/*.sql", recursive=True)
    
    # Copy each file to the _extract directory
    for file_path in sql_files:
        # Get the filename without the path
        file_name = os.path.basename(file_path)
        
        # Copy the file to the _extract directory, overwriting if it exists
        destination = os.path.join("_extract", file_name)
        
        # Copy the file, overwriting if it exists
        shutil.copy2(file_path, destination)
        print(f"Copied: {file_path} -> {destination}")
    
    print(f"Extracted {len(sql_files)} SQL files to the _extract directory")

if __name__ == "__main__":
    extract_sql_files()