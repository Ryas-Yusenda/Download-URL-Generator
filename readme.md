## 🚀 Download URL Generator

**Download URL Generator** is a powerful script that automatically extracts direct download links from various sources. Ideal for users who need quick, reliable access to actual file URLs — whether for batch downloading, automation, or integration into custom workflows.

### ⚡ Features

- Ultra-fast extraction of direct download links
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

   if you want to generate links from **fuckingfast.co**, run:

   ```bash
   python fuckingfast.py
   ```

   or if you want to generate links from **buzzheavier.com**, run:

   ```bash
   python buzzheavier.py
   ```

   or if you want to generate links from **mediafire.com**, run:

   ```bash
    python mediafire.py
   ```

3. The script will extract download links in parallel.
4. Downloaded files will be saved in `links_output.txt`.
5. Done.
