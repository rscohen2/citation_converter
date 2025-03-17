import re


def acm_to_apa(acm_references):
    # List to hold converted APA references
    apa_references = []
    citation_map = {}  # To map citation number to APA in-text citation

    # Regular expression for journal articles
    journal_pattern = r"(?P<authors>[\w\s,\.]+)\. (?P<year>\d{4})\. (?P<title>[^\.]+)\. (?P<journal>[^,]+), (?P<volume>\d+), (?P<issue>\d+) \((?P<year2>\d{4})\), (?P<pages>\d+–\d+)"
    # Regular expression for conference papers with DOI
    conference_doi_pattern = r"(?P<authors>[\w\s,\.]+)\. (?P<year>\d{4})\. (?P<title>[^\.]+)\. In (?P<conference>[^,]+), (?P<pages>[^,]+)\. DOI:(?P<doi>https://[^ ]+)"
    # Regular expression for conference papers without DOI
    conference_pattern = r"(?P<authors>[\w\s,\.]+)\. (?P<year>\d{4})\. (?P<title>[^\.]+)\. In (?P<conference>[^,]+), (?P<pages>[^,]+)\."
    # Regular expression for webpages
    webpage_pattern = r"(?P<website>[^.]+)\. (?P<title>[^.]+)\. Retrieved (?P<retrieved>\w+ \d{1,2}, \d{4}) from (?P<url>https://[^ ]+)"

    # Iterate through each reference to convert it and build the citation map
    for idx, acm_ref in enumerate(acm_references, 118):  # Start numbering from 118
        match = re.search(journal_pattern, acm_ref)
        if match:
            authors = match.group("authors")
            year = match.group("year")
            title = match.group("title")
            journal = match.group("journal")
            volume = match.group("volume")
            issue = match.group("issue")
            pages = match.group("pages")
            apa_ref = f"{authors}. ({year}). {title}. *{journal}*, {volume}({issue}), {pages}."
            apa_references.append(apa_ref)
            citation_map[idx] = f"({authors.split(',')[0]} & {authors.split(',')[1]}, {year})"
            continue

        match = re.search(conference_doi_pattern, acm_ref)
        if match:
            authors = match.group("authors")
            year = match.group("year")
            title = match.group("title")
            conference = match.group("conference")
            pages = match.group("pages")
            doi = match.group("doi")
            apa_ref = f"{authors}. ({year}). {title}. In *{conference}* ({pages}). {doi}"
            apa_references.append(apa_ref)
            citation_map[idx] = f"({authors.split(',')[0]} et al., {year})"
            continue

        match = re.search(conference_pattern, acm_ref)
        if match:
            authors = match.group("authors")
            year = match.group("year")
            title = match.group("title")
            conference = match.group("conference")
            pages = match.group("pages")
            apa_ref = f"{authors}. ({year}). {title}. In *{conference}* ({pages})."
            apa_references.append(apa_ref)
            citation_map[idx] = f"({authors.split(',')[0]} et al., {year})"
            continue

        match = re.search(webpage_pattern, acm_ref)
        if match:
            website = match.group("website")
            title = match.group("title")
            url = match.group("url")
            apa_ref = f"{website}. ({year}). {title}. *{website}*. {url}"
            apa_references.append(apa_ref)
            citation_map[idx] = f"({website}, {year})"

    return apa_references, citation_map


def convert_in_text_citations(text, citation_map):
    # Replace all in-text citations with APA-style in-text citations
    def replace(match):
        citation_number = int(match.group(1))
        if citation_number in citation_map:
            return citation_map[citation_number]
        return match.group(0)

    # Find all instances of [number] and replace them with the APA format
    return re.sub(r"\[(\d+)\]", replace, text)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()


def write_apa_file(apa_text, apa_references, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(apa_references) + "\n\n")
        file.write(apa_text)


# Example usage
acm_file_path = '../Downloads/cscw_consent_pre-print.txt'  # Path to your ACM paper file
apa_file_path = 'apa_paper.txt'  # Path to save the converted APA paper

# Read the content of the paper
acm_text = read_file(acm_file_path)
acm_references = [line.strip() for line in acm_text.split('\n') if line.startswith('[')]  # Extract references

# Convert references and build the citation map
apa_references, citation_map = acm_to_apa(acm_references)

# Convert in-text citations to APA style
apa_text = convert_in_text_citations(acm_text, citation_map)

# Write the converted paper to a new file
write_apa_file(apa_text, apa_references, apa_file_path)

print(f"Converted paper has been saved to {apa_file_path}")
