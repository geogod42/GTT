# GTT (Git to Text)

## Overview
GTT (Git to Text) extracts GitHub repository content into a single text file for easy analysis by large language models. It also extracts images into a separate folder.

## Features
- Clone and extract GitHub repo content.
- Combine README and code files into one text file.
- Exclude files larger than a specified character limit (default: 50,000).
- Extract images into a separate folder.
- Summary includes word count and token count.

## Usage
### Setting up
1. (Optional) Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the required libraries:
   ```sh
   pip install GitPython tqdm
   ```

### Running the Script
To extract contents from a GitHub repo:
```sh
python main.py <github_url> [options]
```

**Example**:
```sh
python main.py https://github.com/torvalds/linux.git -df 0 -maxchar 100000
```

### Command Line Arguments
- `<github_url>`: URL of the GitHub repository.
- `-df, --delete-folder`: (Optional) Delete the downloaded repository folder after extraction. Default is `1` (delete the folder). Set to `0` to retain.
- `-maxchar`: (Optional) Maximum character count per file. Default: `50000`.

## Output
- **Combined Text File**: `<repo_name>_combined.txt` (e.g., `linux_combined.txt`) containing:
  - Repo structure, README content, and relevant files.
- **Images Folder**: Extracted images saved to an `images` folder.
- **Summary**: Word count and estimated token count printed at the end.

## Notes
- Token count is estimated as `2x` the word count.
- The script skips the `.git` folder.

## License
This project is licensed under the MIT License.
