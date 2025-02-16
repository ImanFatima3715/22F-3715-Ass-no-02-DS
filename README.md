# 22F-3715-Ass-no-02-DS

# Research Paper Scraper & Annotation using LLMs

## 📌 Project Overview
This project automates the process of scraping research papers from [NeurIPS](https://papers.nips.cc), storing them locally, and annotating them using a Large Language Model (LLM) API such as Google Gemini. The final dataset includes metadata and an assigned category for each paper, making it easier for researchers to analyze papers offline.

## 🚀 Features
- **Scrapes research papers** from NeurIPS for the last five years.
- **Extracts titles and abstracts** from PDFs.
- **Uses an LLM API** (Google Gemini or OpenAI ChatGPT) to classify papers into five categories.
- **Stores metadata and annotations** in structured CSV files.
- **Supports offline access** to the collected research papers and annotations.

## 📂 Folder Structure
```
📦 research-paper-scraper
 ┣ 📂 data
 ┃ ┣ 📂 pdfs                # Downloaded research papers (PDF format)
 ┃ ┣ 📜 papers_metadata.csv  # Metadata of scraped papers
 ┃ ┣ 📜 annotations          # Category-wise CSV files
 ┃ ┃ ┣ 📜 Deep_Learning.csv
 ┃ ┃ ┣ 📜 Computer_Vision.csv
 ┃ ┃ ┣ 📜 NLP.csv
 ┃ ┃ ┣ 📜 Reinforcement_Learning.csv
 ┃ ┃ ┗ 📜 Optimization.csv
 ┣ 📜 scraper.py             # Script to scrape and download papers
 ┣ 📜 annotate_papers.py      # Script to classify papers using an LLM API
 ┣ 📜 README.md              # Project documentation
```

## 📥 Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/research-paper-scraper.git
   cd research-paper-scraper
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## ⚙️ Configuration
1. **Set up your API Key**
   - Replace `GEMINI_API_KEY` in `annotate_papers.py` with your actual Google Gemini API key.
   ```python
   GEMINI_API_KEY = "your-api-key-here"
   ```

2. **Update file paths**
   - Ensure `BASE_PDF_PATH` and `OUTPUT_CSV` in `annotate_papers.py` point to the correct directories.

## 🏃 Usage
### 1️⃣ Scrape Research Papers
Run the scraper script to download papers from NeurIPS:
```sh
python scraper.py
```

### 2️⃣ Annotate Papers using LLM API
Run the annotation script to classify papers:
```sh
python annotate_papers.py
```

### 3️⃣ View Annotated Papers
- Open `papers_metadata.csv` to see annotated papers.
- Individual category files are stored in `data/annotations/`.

## 📊 Categories Used for Annotation
- **Deep Learning**
- **Computer Vision**
- **Natural Language Processing (NLP)**
- **Reinforcement Learning**
- **Optimization**

## 🔥 Challenges Faced
- **API Connectivity Issues**: Encountered rate limits and quota errors.
- **Handling Large PDF Files**: Extracting structured text was difficult for some PDFs.
- **Library Compatibility**: Ensuring compatibility between Python libraries for scraping and annotation.

## 📖 Blog Post
For an in-depth explanation, check out the [Medium Blog Post](#) (Replace `#` with actual link).

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

---
⚡ **Happy Researching!** 🚀
