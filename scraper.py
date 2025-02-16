import os
import requests
from bs4 import BeautifulSoup

BASE_DIR = "C:\\Users\\Iman Fatima\\Desktop\\Python"  # Main directory
BASE_URL = "https://papers.nips.cc"


def scrape_year(year):
    """Scrapes NeurIPS papers for a given year."""
    year_dir = os.path.join(BASE_DIR, str(year))  # Directory for the year
    os.makedirs(year_dir, exist_ok=True)  # Create if not exists

    url = f"{BASE_URL}/paper_files/paper/{year}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        paper_links = soup.select("li a")  # Extract paper links

        for link in paper_links:
            paper_title = link.text.strip()
            paper_page_url = BASE_URL + link.get("href")

            # Extract authors and PDF link
            paper_response = requests.get(paper_page_url)
            paper_soup = BeautifulSoup(paper_response.text, "html.parser")
            pdf_link = paper_soup.select_one("a[href$='.pdf']")
            authors = extract_authors(paper_soup)

            if pdf_link:
                pdf_url = BASE_URL + pdf_link.get("href")
                file_name = format_filename(paper_title, authors)

                print(f"Downloading: {file_name}")
                download_pdf(pdf_url, file_name, year_dir)
            else:
                print(f"PDF link not found for: {paper_title}")

    except requests.exceptions.RequestException as e:
        print(f"Error scraping year {year}: {e}")


def extract_authors(soup):
    """Extracts authors from the paper page."""
    author_elements = soup.select("meta[name='dc.creator']")
    authors = [author["content"] for author in author_elements]
    return ", ".join(authors)


def format_filename(title, authors):
    """Formats filename safely by replacing special characters."""
    title = "".join(c if c.isalnum() or c in " -_." else "_" for c in title)
    authors = "".join(c if c.isalnum() or c in " -,." else "_" for c in authors)
    return f"{title} - {authors}"


def download_pdf(pdf_url, file_name, year_dir):
    """Downloads the PDF and saves it to the correct folder."""
    try:
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()
        file_path = os.path.join(year_dir, f"{file_name}.pdf")

        with open(file_path, "wb") as pdf_file:
            for chunk in response.iter_content(1024):
                pdf_file.write(chunk)

        print(f"Saved: {file_name}.pdf in {year_dir}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download PDF: {e}")


if __name__ == "__main__":
    for year in range(2019, 2025):  # Loop from 2019 to 2024
        print(f"Scraping papers for year: {year}")
        scrape_year(year)
