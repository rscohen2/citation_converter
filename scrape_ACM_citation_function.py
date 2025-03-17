"possibly building a classifier to identify correct parts of a citation"
import re
import pandas as pd
import spacy
from nbconvert.filters import citation

nlp = spacy.load("en_core_web_sm")

def extract_citation_elements(citation):
    """
    Extract authors, title, journal/conference, and year from a citation using NER.

    Args:
    citation (str): The citation text to be processed.

    Returns:
    dict: A dictionary containing extracted citation elements.
    """

    # Process the citation with spaCy NLP pipeline
    doc = nlp(citation)

    # Initialize variables to hold extracted elements
    authors = []
    journal = ""
    date = ""
# Iterate over the entities detected by spaCy
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Assume that authors are recognized as PERSON
            authors.append(ent.text)
        elif ent.label_ == "ORG":
            # Assume that organizations are journal or conference names
            journal = ent.text
        return authors, journal



# Function to extract citation elements from ACM-style citation
def extract_citation_elements_regex(citation):
    """
    Extract authors, year, title, journal/conference name, volume, issue, pages, and DOI from ACM-style citation.

    Args:
    citation (str): The citation text to be processed.

    Returns:
    dict: A dictionary containing extracted citation elements.
    """

    # Initialize variables to hold extracted elements
    authors = ""
    year = ""
    title = ""
    journal = ""
    volume = ""
    issue = ""
    pages = ""
    doi = ""


    authors, journal = extract_citation_elements(citation)
    # Step 2: Extract the title (usually after the year)
    title_match = re.search(r"\. (\d{4})\.\s([^\.]+)\.\s", citation)
    if title_match:
        title = title_match.group(2).strip()
        # Apply regex to detect the year only if it's in parentheses
    match = re.search(r'\((\d{4})\)', citation)
    if match:
        year = match.group(1)


    # Step 4: Extract DOI (if present)
    doi_match = re.search(r"https://doi.org/[\S]+", citation)
    if doi_match:
        doi = doi_match.group(0)

    # Return extracted citation elements as a dictionary
    return {
        "authors": authors,
        "journal": journal,
        "year": year,
        "title": title,
        "doi": doi
    }


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

if __name__ == "__main__":

    acm_file_path = '../Downloads/cscw_consent_pre-print.txt'  # Path to your ACM paper file
    # Read the content of the paper
    acm_text = read_file(acm_file_path)
    lines = acm_text.split('\n')

    start_line = 369
    end_line = 527
    reference_section = lines[start_line - 1:end_line]

    # acm_references = [line.strip() for line in acm_text.split('\n') if line.startswith('[')]  # Extract references


    # # Extract elements from the reference list
    # extracted_references = extract_from_reference_list(acm_references)
    extracted_references = []
    for reference in reference_section:
        authors, journal, title, year, doi = extract_citation_elements_regex(reference)
        extracted_reference =  {
        "authors": authors,
        "journal": journal,
        "year": year,
        "title": title,
        "doi": doi
    }
        extracted_references.append(extracted_reference)


    df = pd.DataFrame(extracted_references)


    # # Convert the extracted references to a Pandas DataFrame
    # df = pd.DataFrame(extracted_references)
    #
    # # Display the DataFrame
    # print(df)
