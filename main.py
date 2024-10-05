import os
import shutil
import requests
import git
from pathlib import Path
import mimetypes
import argparse
from tqdm import tqdm

# Clones the repository and prints folder structure
def clone_repo(github_url, dest_folder):
    try:
        print("Cloning repository...")
        git.Repo.clone_from(github_url, dest_folder)
        print(f"Repository cloned to {dest_folder}\n")
    except Exception as e:
        print("Incorrect git url format or connection issue.\nUsage: Provide a valid GitHub URL like 'https://github.com/username/repository.git'")
        exit(1)

# Print repository structure
def print_repo_structure(base_folder, indent=0, output_file=None):
    for item in os.listdir(base_folder):
        item_path = os.path.join(base_folder, item)
        line = "  " * indent + f"- {item}\n"
        if output_file:
            output_file.write(line)
        if os.path.isdir(item_path):
            print_repo_structure(item_path, indent + 1, output_file)

# Extract readme and code, saving to a text file
def extract_files(repo_folder, output_folder, repo_name, max_char):
    output_file_path = os.path.join(output_folder, f"{repo_name}_combined.txt")
    all_files = []
    for root, dirs, files in os.walk(repo_folder):
        for file in files:
            all_files.append(os.path.join(root, file))
    
    with open(output_file_path, "w") as output_file:
        # Print repository structure at the top of combined.txt
        output_file.write("\n--- Repository Folder Structure ---\n")
        print_repo_structure(repo_folder, output_file=output_file)
        output_file.write("\n-----------------------------------\n\n")
        
        # Extract and write README file content
        readme_path = None
        for file_name in ["README.md", "README.txt", "readme.md", "readme.txt"]:
            potential_readme = os.path.join(repo_folder, file_name)
            if os.path.isfile(potential_readme):
                readme_path = potential_readme
                break
        if readme_path:
            with open(readme_path, "r") as readme_file:
                output_file.write("\n--- README FILE ---\n")
                output_file.write(readme_file.read())
                output_file.write("\n-------------------\n\n")
        
        # Extract all code with progress bar
        for file_path in tqdm(all_files, desc="Extracting files"):
            # Skip the .git folder
            if ".git" in file_path:
                continue
            # Identify and copy images to the image folder
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('image'):
                copy_image(file_path, output_folder)
            elif file_path.endswith(('.py', '.java', '.c', '.cpp', '.js', '.html', '.css', '.txt', '.md')):
                with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if len(content) <= max_char:
                        output_file.write(f"\n--- File: {file_path.replace(repo_folder, '')} ---\n")
                        output_file.write(content)
                        output_file.write("\n-------------------\n\n")

# Copy image to the output folder
def copy_image(image_path, output_folder):
    images_folder = os.path.join(output_folder, "images")
    os.makedirs(images_folder, exist_ok=True)
    shutil.copy(image_path, images_folder)

# Main function
def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Extract GitHub repository contents into a single text file.")
    parser.add_argument("github_url", help="GitHub repository URL")
    parser.add_argument("-df", "--delete-folder", type=bool, default=True, help="Delete the download ed repository folder after extraction (default: True)")
    parser.add_argument("-maxchar", type=int, default=50000, help="Maximum character count per file to include in extraction (default: 50,000)")
    args = parser.parse_args()
    
    # Derive repository name from URL
    repo_name = args.github_url.rstrip(".git").split("/")[-1]
    output_folder = f"{repo_name}_GTT"
    dest_folder = "repo"
    
    # Cleanup folders if they already exist
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Clone the repository
    clone_repo(args.github_url, dest_folder)

    # Create output folder only if cloning was successful
    os.makedirs(output_folder, exist_ok=True)

    # Extract files
    extract_files(dest_folder, output_folder, repo_name, args.maxchar)
    print(f"\nAll code and README files have been extracted to {output_folder}/{repo_name}_combined.txt")
    print(f"Images have been extracted to {output_folder}/images folder")

    # Optionally delete the downloaded repository folder
    if args.delete_folder == 1:
        shutil.rmtree(dest_folder)
        print(f"\nDeleted the repository folder: {dest_folder}")

    # Summary of extraction
    combined_file_path = os.path.join(output_folder, f"{repo_name}_combined.txt")
    with open(combined_file_path, "r") as combined_file:
        combined_content = combined_file.read()
        word_count = len(combined_content.split())
        token_count = word_count * 2
    print(f"\nSummary: The {repo_name}_combined.txt file contains {word_count} words.")
    print(f"Token count (estimated as 2x word count): {token_count} tokens.\nNote: This is a rough estimate and may vary depending on actual tokenization.")

if __name__ == "__main__":
    main()