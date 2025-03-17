"functions to convert the in-text citations from ACM to APA format"

import re

def identify_in_text_citations(text, start_line, end_line):
        # Split the text into lines
        lines = text.split('\n')

        # Slice the text between start_line and end_line (inclusive)
        lines_to_search = lines[start_line - 1:end_line]  # Adjust for 0-based indexing

        # Join the selected lines back into a single string
        text_to_search = "\n".join(lines_to_search)

        # Regular expression pattern to match citations in the form of [28] or (28)
        pattern = r"\[(\d+(?:,\d+)*)\]"  # Matches numbers in square brackets, with optional comma-separated numbers

        # Find all matches of the pattern
        matches = re.findall(pattern, text_to_search)

        # # Extract the matched citation numbers from the tuples
        # citations = [match[0] if match[0] else match[1] for match in matches]

        return matches

def parse_acm_in_text(acm_in_text):
    acm_in_text = acm_in_text.strip('[')
    acm_in_text = acm_in_text.strip(']')
    acm_in_text = acm_in_text.strip('.')
    acm_in_text = acm_in_text.strip(']')
    acm_in_text = acm_in_text.split(',')
    return acm_in_text

def convert_in_text_citations(text, citation_map):
    text = parse_acm_in_text(text)
    apa_citations = []
    for number in text:
        citation = citation_map[number]
        apa_citations.append(citation)
    return apa_citations


def create_citation_map(references):
    # Split the text into lines
    # references_start_index = 368
    # # Extract only the part of the text that comes after the "References" section
    # references = '\n'.join(lines[references_start_index + 1:])
    # print(references[0])
    # Create a dictionary to hold author names and citations
    author_citation_map = {}
    # Regex to match authors and their citation (simple for the example)
    pattern = r"\[(\d+)\]\s*(.*)"
    reference_map = {}
    for line in references[1:]:
        # Match each line with the pattern
        match = re.match(pattern, line)
        if match:
            ref_number = match.group(1)  # The reference number in square brackets
            citation = match.group(2)  # The full citation after the number

            # Add the reference number and citation to the map
            reference_map[ref_number] = citation

    return reference_map

def make_full_reference_in_text(full_reference):
    # Regular expression to match authors and year in the full reference
    author_pattern = r"^([A-Za-z,.\s&]+)\s\((\d{4})\)"

    # Search for the authors and year in the reference
    match = re.match(author_pattern, full_reference)

    if match:
        authors = match.group(1).strip()  # Extract authors
        year = match.group(2)  # Extract year

        # Remove any "et al." if it's present for multiple authors
        if 'et al.' in authors:
            authors = authors.split(' et al.')[0]

        # Create in-text citation in the format (Author, Year) or (First Author et al., Year)
        # If there are multiple authors, we can use "et al."
        authors_list = authors.split(',')
        if len(authors_list) > 3:
            in_text_citation = f"({authors_list[0]} et al., {year})"
        else:
            in_text_citation = f"({authors}, {year})"

        return in_text_citation
    else:
        return None  # If the pattern doesn't match, return None


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

# def full_in_text_conversion(acm_lines):
#     acm_references = identify_in_text_citations(acm_lines, 14, 360)
#     citation_map = create_citation_map(acm_references)
#     new_in_text_refs = []
#     for reference in acm_references:
#         in_text = convert_in_text_citations(acm_references, citation_map)
#         new_in_text_refs.append(in_text)
#     return new_in_text_refs


# def replace_in_text_citations(text, citation_map):
#     # Regular expression pattern to match in-text citations in the form of [28], [12,13,16]
#     pattern = r"\[(\d+(?:,\d+)*)\]"
#
#     # Function to replace a match with the corresponding reference from the citation_map
#     def replace_citation(match):
#         citation_id = match.group(1)  # Extract the citation number (e.g., "28", "12,13,16")
#
#         # Get the corresponding full reference from the citation_map
#         reference = citation_map.get(citation_id)
#
#         if reference:
#             return reference  # Return the full reference
#         else:
#             return match.group(0)  # If not found, return the original citation (e.g., [28])
#
#     # Replace all occurrences of in-text citations in the text using the replace_citation function
#     replaced_text = re.sub(pattern, replace_citation, text)
#
#     return replaced_text


# Function to replace a match with the corresponding reference from the citation_map
def replace_citation(match, citation_map):
    converted_references = []
    references = []
    citation_id = match.group(1)  # Extract the citation number (e.g., "28", "12,13,16")
    for id in citation_id:
        reference = citation_map.get(citation_id)
        references.append(reference)
    if references:
        # If there are multiple references, join them with commas
        if isinstance(references, list):
            formatted_references = [f"({ref})" for ref in references]
            return ", ".join(formatted_references)
        else:
            # Otherwise, just return the single reference formatted
            return f"({references})"
    else:
        return match.group(0)  # If no reference found, return the original citation


def replace_in_text_citations_within_range(text, citation_map, start_line, end_line):

    # Slice the text between start_line and end_line (inclusive)
    lines = text.split('\n')

    lines_to_search = lines[start_line:end_line]
    text_to_search = "\n".join(lines_to_search)

    # Join the selected lines back into a single string
    # text_to_search = "\n".join(lines_to_search)

    # # Regular expression pattern to match citations in square brackets [12], [12,13,16]
    # pattern = r"\[(\d+(?:,\d+)*)\]"
    # matches = re.findall(pattern, text_to_search)

    # Regular expression to match citations in square brackets [12], [12,13,16]
    pattern = r"\[(\d+(?:,\d+)*)\]"

    # Split the text into lines and focus on the range of lines to process
    lines = text.split('\n')
    text_to_search = "\n".join(lines[start_line - 1:end_line])  # Adjust for 0-based indexing

    # Replace in-text citations with references
    replaced_text = re.sub(pattern, lambda match: replace_citation(match, citation_map), text_to_search)

    # Rebuild the full text by replacing the specified range with the modified version
    lines[start_line - 1:end_line] = replaced_text.split('\n')
    final_text = "\n".join(lines)

    # Return the modified text only if it's different from the original text_to_search
    return final_text if final_text != text_to_search else text_to_search




if __name__ == "__main__":

    acm_file_path = '../Downloads/cscw_consent_pre-print.txt'  # Path to your ACM paper file
    # Read the content of the paper
    acm_text = read_file(acm_file_path)
    acm_references = [line.strip() for line in acm_text.split('\n') if line.startswith('[')]  # Extract references
    citation_map = create_citation_map(acm_references)
    in_text_citations = identify_in_text_citations(acm_text, 14, 360)


    new_file = replace_in_text_citations_within_range(acm_text, citation_map, 13, 360)
    print(new_file)
    # acm =  '[32,33,122].'
    # in_text = convert_in_text_citations(acm, citation_map)
    # print(in_text)