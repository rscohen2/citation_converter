from acm_to_apa import acm_to_apa, replace_reference_section_with_modified
import convert_in_text
import re

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

# def clean_line(line):
#     words = []
#     for word in line.split():
#         word =  "".join(ch for ch in word if ch.isalnum())
#         words.append(word)
#     clean_line = " ".join(words)
#     return clean_line

# def clean_line(line):
#     # Define the pattern for valid characters (letters, numbers, and punctuation)
#     valid_chars_pattern = re.compile(r"[a-zA-Z0-9.,!?;:'\"()\-]")
#
#     words = []
#     for word in line.split():
#         # Only keep valid characters (alphanumeric + selected punctuation)
#         cleaned_word = "".join(ch for ch in word if valid_chars_pattern.match(ch))
#
#         # Add the cleaned word if it's not empty
#         if cleaned_word:
#             words.append(cleaned_word)
#
#     # Join cleaned words back into a line
#     cleaned_line = " ".join(words)
#     return cleaned_line

import re


def clean_line(line):
    # Define a pattern that includes alphanumeric characters and selected punctuation

    line = line.replace('�', '')
    valid_chars_pattern = re.compile(r"[a-zA-Z0-9.,!?;:'\"()\-]")

    # Create a list to store cleaned words
    cleaned_words = []
    for word in line.split():
        # Clean the word by filtering valid characters
        cleaned_word = "".join(ch for ch in word if valid_chars_pattern.match(ch))

        if cleaned_word:
            cleaned_words.append(cleaned_word)
        else:
            # If word is entirely invalid characters, append an empty string
            cleaned_words.append('')

    # Join cleaned words and return the cleaned line
    return " ".join(cleaned_words)


def clean_text(text):
    # Split the text into lines to maintain line breaks
    lines = text.split('\n')

    # Clean each line while preserving line breaks
    cleaned_lines = [clean_line(line) for line in lines]

    # Rejoin cleaned lines with newlines to maintain the format
    return "\n".join(cleaned_lines)


# def write_apa_file(apa_text, apa_references, output_file_path):
#     with open(output_file_path, 'w', encoding='utf-8') as file:
#         file.write("\n".join(apa_references) + "\n\n")
#         file.write(apa_text)

def convert_references_to_apa(acm_references):
    converted_refs = []
    for reference in acm_references:
        acm_to_apa(reference)
    return converted_refs




# Example usage
acm_file_path = '../Downloads/cscw_consent_pre-print.txt'  # Path to your ACM paper file
apa_file_path = 'apa_paper.txt'  # Path to save the converted APA paper

# Read the content of the paper
acm_text = read_file(acm_file_path)
lines = acm_text.split('\n')

clean_text = clean_text(acm_text)

acm_references = [line.strip() for line in lines if line.startswith('[')]  # Extract references
citation_map = convert_in_text.create_citation_map(acm_references)

#convert in_text citations
new_file = convert_in_text.replace_in_text_citations_within_range(acm_text, citation_map, 13, 360)

output_file_path = 'converted_apa_paper_INTEXT.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(new_file)

new_file_path = 'converted_apa_paper_INTEXT.txt'
acm_text = read_file(new_file_path)


modified_file = replace_reference_section_with_modified(acm_text, 368, 527)

#convert references section
# converted_refs = convert_references_to_apa(acm_references)

#create the output file

output_file_path = 'converted_apa_paper.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(modified_file)


print(f"Converted paper has been saved to {apa_file_path}")