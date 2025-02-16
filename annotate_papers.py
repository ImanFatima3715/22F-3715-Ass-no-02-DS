import os
import time
import shutil
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai  # Google Gemini API
import pandas as pd

# 🏢 Define base directory for PDFs (Must be a folder, not a single file)
BASE_PDF_PATH = r"C:\Users\Iman Fatima\Desktop\Python\scraper.pdf"  # Update to the correct folder path
OUTPUT_DIR = r"C:\Users\Iman Fatima\Desktop\Python\paper_data.csv"  # Base directory for category-wise CSV files

# 🔑 Google Gemini API Key (Replace with your actual API key)
GEMINI_API_KEY = "AIzaSyACR4sGAjNECzoc4MopghV5TyvaLyieUGs"
if not GEMINI_API_KEY:
    print("❌ Google Gemini API Key is missing! Please update GEMINI_API_KEY.")
    exit(1)

# ✅ Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# 🎯 Define Five Research Categories
CATEGORIES = [
    "Deep Learning",
    "Computer Vision",
    "Natural Language Processing",
    "Reinforcement Learning",
    "Optimization"
]

CATEGORY_FILES = {category: os.path.join(OUTPUT_DIR, f"{category}.csv") for category in CATEGORIES}

def find_pdfs_in_directory(directory):
    """Recursively finds all PDF files in the given directory and its subdirectories."""
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def extract_text_from_pdf(pdf_path):
    """Extracts title and abstract from the first page of a PDF."""
    try:
        doc = fitz.open(pdf_path)
        if len(doc) == 0:
            print(f"⚠ {pdf_path} is empty or unreadable.")
            return None, None

        text = doc[0].get_text("text")  # Extract first page text
        doc.close()

        if not text.strip():
            print(f"⚠ {pdf_path} has no readable text.")
            return None, None

        title = os.path.basename(pdf_path).replace(".pdf", "").replace("_", " ")
        abstract = text[:500]  # Extract first 500 characters for classification

        return title, abstract
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return None, None

def classify_paper(title, abstract):
    """Classifies the paper using Google Gemini API with retry mechanism."""
    prompt = f"""Classify the following research paper into one of these categories: {', '.join(CATEGORIES)}.
        
Title: {title}
Abstract: {abstract}

Category:"""

    model = genai.GenerativeModel("gemini-pro")

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = model.generate_content(prompt)
            time.sleep(2)  # Add delay to avoid hitting API rate limits
            return response.text.strip()
        except Exception as e:
            print(f"⚠ API Error (Attempt {attempt+1}/3): {e}")
            if "quota" in str(e).lower() or "exhausted" in str(e).lower():
                print("🚨 API quota exceeded! Waiting before retrying...")
                time.sleep(30)  # Wait before retrying
            else:
                break

    return "Unknown"

def save_to_csv(papers_metadata):
    """Saves classified papers into category-specific CSV files."""
    try:
        categorized_data = {category: [] for category in CATEGORIES}
        categorized_data["Unknown"] = []  # Handle unknown classifications

        for title, abstract, category, filename in papers_metadata:
            if category in categorized_data:
                categorized_data[category].append([title, abstract, category, filename])
            else:
                categorized_data["Unknown"].append([title, abstract, "Unknown", filename])

        for category, data in categorized_data.items():
            file_path = CATEGORY_FILES.get(category, os.path.join(OUTPUT_DIR, "Unknown.csv"))
            df = pd.DataFrame(data, columns=["Title", "Abstract", "Category", "PDF File"])

            if os.path.exists(file_path):
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(file_path, index=False)

            print(f"📄 Data saved in: {file_path} (Total: {len(df)})")

    except PermissionError:
        print("❌ Permission error: Cannot write to CSV files. Close any open files and try again.")
    except Exception as e:
        print(f"❌ Error saving category-wise CSV files: {e}")

def process_papers(batch_size=5, daily_limit=50):
    """Processes PDFs in smaller batches to avoid exceeding API limits."""
    if not os.path.exists(BASE_PDF_PATH):
        print(f"❌ Directory not found: {BASE_PDF_PATH}")
        return

    print(f"🔍 Scanning for PDFs in {BASE_PDF_PATH} and its subfolders...")
    pdf_files = find_pdfs_in_directory(BASE_PDF_PATH)

    if not pdf_files:
        print("⚠ No PDF files found. Please check the folder structure.")
        return

    print(f"📂 Found {len(pdf_files)} PDFs")

    papers_metadata = []
    processed_count = 0

    for i in range(0, min(len(pdf_files), daily_limit), batch_size):
        batch_files = pdf_files[i:i+batch_size]
        print(f"\n🚀 Processing batch {i//batch_size + 1} (Files: {len(batch_files)})...\n")

        for pdf_path in batch_files:
            filename = os.path.basename(pdf_path)
            print(f"📖 Processing: {filename}...")

            title, abstract = extract_text_from_pdf(pdf_path)
            if title and abstract:
                category = classify_paper(title, abstract)
                papers_metadata.append([title, abstract, category, filename])
                print(f"✔ Annotated: {title} → {category}")
                processed_count += 1
                if processed_count >= daily_limit:
                    print("⏸️ Daily API limit reached! Stopping processing.")
                    save_to_csv(papers_metadata)
                    return

        save_to_csv(papers_metadata)

if __name__ == "__main__":
    print("🔎 Starting PDF annotation process...")
    process_papers(batch_size=5, daily_limit=50)  # Process 50 PDFs per day to avoid quota issues
    print("✅ Annotation process completed!")
