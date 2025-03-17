
"""The script to convert the full reference section from ACM to APA
I think there are still some errors present in the elements where paranthesis are added to titles instead of the year etc, which I will need to clean up a bit.
"""


import re

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

def acm_to_apa(citation):
    # Regex pattern to capture parts of a more complex ACM citation
    citation = re.sub(r"^\[\d+\]\s*", "", citation)
    strict_pattern = r"([A-Za-z\., ]+?)\.\s*(\d{4})\.\s*([^\.]+?)\.\s*(In\s*[^,]+,|[^\.]+)?\s*(\d+–\d+|\d+)?\."

    match = re.match(strict_pattern, citation)

    if match:
        authors = match.group(1).strip() if match.group(1) else ""
        additional_authors = match.group(2).strip() if match.group(2) else ""
        year = match.group(3) if match.group(3) else ""
        title = match.group(4) if match.group(4) else ""
        proceedings = match.group(5).strip() if match.group(5) else ""
        # page_range = match.group(6) if match.group(6) else ""

        # Combine authors if there's more than one part
        if additional_authors:
            authors = f"{authors}, {additional_authors}"

        # APA format citation construction
        apa_citation = f"{authors} ({year}). {title}. {proceedings}"
        return apa_citation

    else:
        # If no match is found with the strict pattern, try the lenient pattern for simpler citations
        fallback_pattern = r"([A-Za-z, ]+?)\.\s*(\d{4})\.\s*([^\.]+?)(?:\.\s*(In\s*([^,]+?),\s*)?(\d+–\d+|\d+)?\.)?"

        match = re.match(fallback_pattern, citation)

        if match:
            authors = match.group(1).strip() if match.group(1) else ""
            year = match.group(2) if match.group(2) else ""
            title = match.group(3) if match.group(3) else ""
            proceedings = match.group(4).strip() if match.group(4) else ""
            page_range = match.group(5) if match.group(5) else ""

            # APA format citation construction
            apa_citation = f"{authors} ({year}). {title}. {proceedings}"
            return apa_citation
        else:
            # New fallback pattern for specific case: Proceedings without page numbers or with different formatting
            specific_fallback_pattern = r"([A-Za-z, ]+?)\.\s*(\d{4})\.\s*([^\.]+?)\.\s*(In\s*[^,]+,\s*[^,]+(?:\s*[\d–]+\d+)+)?"  # Handling Proceedings with page range

            match = re.match(specific_fallback_pattern, citation)

            if match:
                authors = match.group(1).strip() if match.group(1) else ""
                year = match.group(2) if match.group(2) else ""
                title = match.group(3) if match.group(3) else ""
                proceedings = match.group(4).strip() if match.group(4) else ""
                page_range = match.group(5) if match.group(5) else ""

                # APA format citation construction
                apa_citation = f"{authors} ({year}). {title}. {proceedings}"
                return apa_citation

            else:
                return ""



def replace_citation(match):
    acm_citation = match.group(0)  # Original ACM citation as a string
    apa_citation = acm_to_apa(acm_citation[1:-1])  # Remove the square brackets and convert to APA
    return f"({apa_citation})"  # Wrap the APA citation in parentheses



def replace_acm_citations_with_apa(text_to_search):
    # Regular expression to match ACM citation in the format [Author. Year. Title...]
    # lines = text.split('\n')
    #
    # lines_to_search = lines[start_line:end_line]
    # text_to_search = "\n".join(lines_to_search)

    # pattern = r"\[([A-Za-z, ]+)\. (\d{4})\. ([^\.]+)\. In ([^,]+), Vol\. (\d+), ([^,]+), Article (\d+), (\d{4})\. ACM, ([^\.]+)\. (\d+ pages)\. https://doi.org/([^ ]+)\]"


    #
    # # Split the text into lines
    # lines = text.split('\n')
    #
    # text_to_search = "\n".join(lines[start_line - 1:end_line])  # Adjust for 0-based indexing


    # Get the lines in the range [start_line - 1:end_line] (adjusting for 0-based indexing)
    # lines_to_process = lines[start_line - 1:end_line]

    # Replace ACM citations in the selected lines with APA format
    # replaced_text = re.sub(pattern, replace_citation, text_to_search)

    # # Rebuild the full text by replacing the original range with the modified version
    # lines[start_line - 1:end_line] = replaced_text

    # Rebuild the full text by replacing the specified range with the modified version
    replaced_text = []
    # lines[start_line - 1:end_line] = replaced_text.split('\n')
    for line in text_to_search.split('\n'):
        apa_line = (acm_to_apa(line))
        replaced_text.append(apa_line)

    # Join the replaced lines back into a single string
    return "\n".join(replaced_text)


def replace_reference_section_with_modified(text, start_line, end_line):
    # Split the text into lines
    lines = text.split('\n')

    # Extract the lines corresponding to the reference section
    reference_section = lines[start_line - 1:end_line]

    # Apply the ACM to APA conversion to the reference section
    modified_reference_section = replace_acm_citations_with_apa("\n".join(reference_section))

    # Replace the reference section in the original text with the modified version
    lines[start_line - 1:end_line] = modified_reference_section.split('\n')

    # Join the lines back into a single string
    final_text = "\n".join(lines)

    return final_text


if __name__ == "__main__":
    #test out function with an example
    # # Example usage
    # acm_citation = "Douglas Zytko, Nicholas Furlo, Bailey Carlin, Matthew Archer. 2021. Computer-Mediated Consent to Sex: The Context of Tinder. In Proceedings of the ACM on Human-Computer Interaction, Vol. 5, CSCW1, Article 189, 2021. ACM, New York, NY, USA. 27 pages. https://doi.org/10.1145/3449288 "
    # apa_citation = acm_to_apa(acm_citation)
    # print(apa_citation)


    acm_file_path = '../Downloads/cscw_consent_pre-print.txt'  # Path to your ACM paper file
    # Read the content of the paper
    acm_text = read_file(acm_file_path)
    acm_references = [line.strip() for line in acm_text.split('\n') if line.startswith('[')]  # Extract references
    # new_file = replace_acm_citations_with_apa(acm_text, 368, 527)
    # print(new_file)

    modified_file = replace_reference_section_with_modified(acm_text, 368, 527)
    print(modified_file)

    #TODO: fix the start/end line discrepencies
#
# citation = 'Syed Ishtiaque Ahmed, Steven J Jackson, Nova Ahmed, Hasan Shahid Ferdous, Md Rashidujjaman Rifat, A S M Rizvi, Shamir Ahmed, and Rifat Sabbir Mansur. 2014. Protibadi: A platform for fighting sexual harassment in urban Bangladesh. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems, 2695–2704.'
# pattern = r"([A-Za-z, ]+?),?\s*(\d{4})\.\s*([^\.]+?)\.\s*In\s*([^,]+?),\s*([\d–]+)"
# match = re.match(pattern, citation)
#
# acm_citation = "[1] Syed Ishtiaque Ahmed, Steven J Jackson, Nova Ahmed, Hasan Shahid Ferdous, Md Rashidujjaman Rifat, A S M Rizvi, Shamir Ahmed, and Rifat Sabbir Mansur. 2014. Protibadi: A platform for fighting sexual harassment in urban Bangladesh. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems, 2695–2704."
# apa_citation = acm_to_apa(acm_citation)
# print(apa_citation)