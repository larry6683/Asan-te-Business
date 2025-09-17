import os
import shutil
import sys

def extract_files():
    # Create the output directory
    output_dir = "_extract"
    
    # Check for "clear" command line argument
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print(f"Cleared {output_dir} directory")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get current working directory
    working_dir = os.getcwd()
    
    # Set the source directory to 'src'
    src_dir = os.path.join(working_dir, "src")
    
    # Check if src directory exists
    if not os.path.exists(src_dir):
        print(f"Error: 'src' directory not found in {working_dir}")
        return
    
    # Walk through all directories and files starting from src directory
    for root, dirs, files in os.walk(src_dir):        
        # Skip src/codegen directory
        if os.path.normpath(root).startswith(os.path.normpath(os.path.join(src_dir, "codegen"))):
            continue
        
        for file in files:
            # Check if file has .proto or .py extension
            if file.endswith(('.proto', '.py')):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, src_dir)
                
                # Skip config/local_config.py (relative to src)
                if os.path.normpath(relative_path) == os.path.normpath(os.path.join("config", "local_config.py")):
                    continue
                
                # Copy the file to flat structure (overwrites if exists)
                dest_path = os.path.join(output_dir, file)
                shutil.copy2(source_path, dest_path)
                print(f"Copied: {file}")

    print(f"\nExtraction complete! Files copied to: {output_dir}")

if __name__ == "__main__":
    extract_files()