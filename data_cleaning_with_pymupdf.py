import re
from pymupdf_text_extraction import TextExtractionWithPyMuPDF
from pathlib import Path

document_file = "Math-for-Programmers.pdf"

def remove_pdf_artifacts(text):
    artifacts = [
    ]

    for artifact in artifacts:
        text = text.replace(artifact, "")
    return text
def normalize_whitespace(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove excessive spaces inside a line
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove spaces at beginning/end of each line
    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)

def remove_standalone_page_numbers(text):

    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:

        # Remove lines containing only numbers
        if re.fullmatch(r"\d+", line):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_excessive_blank_lines(text):

    # Convert 3 or more newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()



def clean_text(text):

    # Step 1
    text = remove_pdf_artifacts(text)

    # Step 2
    text = normalize_whitespace(text)

    # Step 3
    text = remove_standalone_page_numbers(text)

    # Step 4
    text = remove_excessive_blank_lines(text)

    return text



print("Extracting PDF text...")

pymupdf_pages = TextExtractionWithPyMuPDF.text_extraction(
    document_file
)



cleaned_pages = []

for page in pymupdf_pages:

    page_number = page["page"]

    raw_text = page["text"]

    # Use our reusable cleaning function
    cleaned = clean_text(raw_text)

    cleaned_pages.append({
        "page": page_number,
        "text": cleaned
    })


print("Cleaning complete.")

print("Saving cleaned pages...")

# Save beside this script, regardless of the terminal's current directory.
script_folder = Path(__file__).resolve().parent
chunks_folder = script_folder / "chunks"
chunks_folder.mkdir(parents=True, exist_ok=True)

for page in cleaned_pages:
    output_file = chunks_folder / f"page_{page['page']}.txt"
    output_file.write_text(page["text"], encoding="utf-8")

print(f"Saved {len(cleaned_pages)} page files in: {chunks_folder}")
