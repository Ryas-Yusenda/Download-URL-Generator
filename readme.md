
# 🚀 Download URL Generator

**Download URL Generator** is a modular script that automatically extracts direct download links from various file hosting providers.  
It now supports **dynamic handlers** for each domain, so you only need to maintain one central script.

---

## ⚡ Features

- Automatically detects and processes links based on domain
- Supports mixed input (raw URLs or HTML snippets) via `links.txt`
- Async processing for faster extraction
- Clean and extensible handler-based architecture
- Saves all results into `links_output.txt`

---

## 🛠 Prerequisites

1. Install [Python 3.x](https://www.python.org/downloads/).

---

## 🔧 How It Works

1. Add links to `links.txt`  
   - Can be **raw URLs**:
     ```txt
     https://buzzheavier.com/3x4mpl31ink1
     https://fuckingfast.co/3x4mpl31ink2
     https://www.mediafire.com/file/3x4mpl31ink3/example.7z/file
     https://pixeldrain.com/u/3x4mpl31ink4
     ```
   - Or **HTML content** with links:
     ```html
     <a href="https://fuckingfast.co/3x4mpl31ink5">File</a>
     <a href="https://fuckingfast.co/3x4mpl31ink6">File</a>
     ```

2. Run the main script:

   ```bash
   python process.py
   ```

3. The script will:
   - Parse `links.txt` and extract all valid URLs
   - Match each URL with its corresponding domain handler
   - Retrieve direct download links in parallel
   - Save results to `links_output.txt`
