#!/usr/bin/env python3
from pypdf import PdfReader, PdfWriter
import requests
import os
import re

def download_pdf(url, temp_path="temp.pdf"):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    with open(temp_path, 'wb') as f:
        f.write(response.content)
    return temp_path

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Add empty string if None
    return text

def save_text_to_file(text, output_path="output.txt"):
    with open(output_path, 'w') as f:
        f.write(text)

def replace_by_regex(text, regex, replacement):
    """
    replace all occurrences of the text matching the provided regex pattern.
    """
    return re.sub(regex, replacement, text)

def replace_by_string(text, string, replacement):
    """
    replace all occurrences of the provided string.
    """
    return text.replace(string, replacement)

def beautify_text(text):
    # Remove time patterns like nn:nn-nn:nn
    text = replace_by_regex(text, r'\d{1,2}:\d{2}-\d{1,2}:\d{2}', '') # Remove time patterns
    text = replace_by_string(text, 'Der Sportunterricht beginnt und endet 20 Minuten später als in diesem Stundenplan angegeben', '') # Remove specific string
    text = replace_by_string(text, 'LehrpersonModulZimmer', '') # Remove 'LehrpersonModulZimmer' string
    text = replace_by_string(text, 'Schultag', '') # Remove 'Schultag' string
    text = replace_by_regex(text, r'\d{1,2}\.\d{1,2}\.\d{2,4}', '')  # Remove dates
    text = replace_by_regex(text, r'Sport \d', '')  # remove 'Sport \d' # Remove 'Sport 1', 'Sport 2', etc.
    text = replace_by_string(text, 'Hinweis zum Sport:', '')  # Remove 'Hinweis zum Sport:'
    text = replace_by_string(text, 'Stundenplan der KlasseBlock :', '')  # Remove 'Stundenplan der KlasseBlock :'
    text = replace_by_string(text, 'Klassenlehrperson', '')  # Remove 'Klassenlehrperson'
    text = replace_by_string(text, 'Stundenplan der KlasseBlock ', '')  # Remove 'Lehrperson'
    text = replace_by_regex(text, r'Seite \d?\d von \d\d', '')  # Remove 'Seite x von xx'
    text = replace_by_regex(text, r'Seite \d?', '')  # remove 'Seite x'
    text = replace_by_regex(text, r'([A-Z]{4})', r'\n\1\n')  # Add space BEFORE AND AFTER four capital letters
    text = replace_by_regex(text, r'8[a-zA-Z0-9]{5,7}', r'CLASS HERE')  # /8[a-zA-Z0-9]{5,7}/g ->  | 85ia22d -> 5ia22d
    # ACTUAL JSONIFICATION
    text = replace_by_regex(text, r':', '')  # Remove colons
    return text

def main():
    pdf_url = 'https://bbw.ch/wp-content/uploads/2025/05/Stundenplan_Block_8_FS25_V1.pdf'
    temp_pdf_path = "downloaded_schedule.pdf"
    output_txt_path = "schedule_text.txt"

    print(f"Downloading PDF from {pdf_url}...")
    downloaded_pdf_file = download_pdf(pdf_url, temp_pdf_path)
    print(f"PDF downloaded to {downloaded_pdf_file}")

    reader = PdfReader(downloaded_pdf_file)
    total_pages = len(reader.pages)
    print(f"PDF has {total_pages} pages. Processing each page separately...")

    # Process and beautify each page individually
    with open(output_txt_path, 'w') as outfile:
        for i, page in enumerate(reader.pages, start=1):
            page_pdf_path = f"page_{i}.pdf"
            writer = PdfWriter()
            writer.add_page(page)
            with open(page_pdf_path, 'wb') as pf:
                writer.write(pf)
            print(f"Processing page {i}...")
            raw_text = extract_text_from_pdf(page_pdf_path)
            beautified = beautify_text("---\n"+raw_text+"\n")
            outfile.write(beautified)
            os.remove(page_pdf_path)

    # Clean up
    os.remove(downloaded_pdf_file)
    print(f"All pages processed and output saved to {output_txt_path}")
    print("Process completed successfully.")

if __name__ == "__main__":
    main()

