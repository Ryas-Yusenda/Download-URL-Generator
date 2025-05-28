## 🚀 FuckingFast Batch

**FuckingFast Batch** is a blazing-fast batch download script designed to fetch multiple files in record time. Perfect for users who demand extreme download speed, automation, and simplicity — all in one tool.

### ⚡ Features

- Ultra-fast parallel downloading
- Lightweight and easy to use
- Supports a list of URLs or HTML files via `links.txt`

### 🛠 Prerequisites

1. Python 3.x installed on your system. download it from [python.org](https://www.python.org/downloads/).
2. Install the required libraries by running:

   ```bash
   pip install -r requirements.txt
   ```

### 🔧 How It Works

1. Add a list of URLs or an HTML file containing links to `links.txt`.

   - Example (links.txt with URLs):
     ```txt
     https://fuckingfast.co/3x4mpl31ink1
     https://fuckingfast.co/3x4mpl31ink2
     ```
   - Or, if you have an HTML file:
     ```html
     <!DOCTYPE html>
     <html lang="en">
       <head>
         <meta charset="UTF-8" />
         <title>Links</title>
       </head>
       <body>
         <a href="https://fuckingfast.co/3x4mpl31ink1">File 1</a>
         <a href="https://fuckingfast.co/3x4mpl31ink2">File 2</a>
       </body>
     </html>
     ```

2. Run the script using:

   ```bash
   python fuckingfast.py
   ```

3. The script will extract download links in parallel.
4. Downloaded files will be saved in `links_output.txt`.
5. Done.
