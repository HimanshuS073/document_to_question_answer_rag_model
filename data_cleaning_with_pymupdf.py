import re

from pymupdf_text_extraction import TextExtractionWithPyMuPDF


# ============================================================
# CONFIGURATION
# ============================================================

document_file = "Math-for-Programmers.pdf"


# ============================================================
# PDF TEXT CLEANING FUNCTIONS
# ============================================================

def remove_pdf_artifacts(text):
    """
    Remove repeated PDF headers/footers and publishing artifacts.
    """

    artifacts = [
        "Manning Publications Co.",
        "To comment go to liveBook",
        "MEAP Edition",
        "Manning Early Access Program",
    ]

    for artifact in artifacts:
        text = text.replace(artifact, "")

    return text


def normalize_whitespace(text):
    """
    Clean unnecessary spaces and line formatting
    without destroying the overall structure.
    """

    # Normalize line endings
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
    """
    Remove lines that contain only a page number.

    Example:
        172

    But this does NOT remove numbers appearing inside
    normal sentences or code.
    """

    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:

        if re.fullmatch(r"\d+", line):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_excessive_blank_lines(text):
    """
    Keep a maximum of one blank line between sections.
    """

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_text(text):
    """
    Complete cleaning pipeline.
    """

    text = remove_pdf_artifacts(text)

    text = normalize_whitespace(text)

    text = remove_standalone_page_numbers(text)

    text = remove_excessive_blank_lines(text)

    return text


# ============================================================
# EXTRACT TEXT USING PYMUPDF
# ============================================================

print("Extracting PDF text...")

pymupdf_pages = TextExtractionWithPyMuPDF.text_extraction(
    document_file
)

print(f"Extracted {len(pymupdf_pages)} pages.")


# ============================================================
# CLEAN EACH PAGE
# ============================================================

cleaned_pages = []

print("Cleaning text...")

for page in pymupdf_pages:

    page_number = page["page"]
    raw_text = page["text"]

    cleaned_text = clean_text(raw_text)

    cleaned_pages.append({
        "page": page_number,
        "text": cleaned_text
    })


print("Cleaning complete.")


# ============================================================
# DISPLAY CLEANED TEXT
# ============================================================

for page in cleaned_pages:

    print("\n" + "=" * 80)
    print(f"PAGE: {page['page']}")
    print("=" * 80)

    print(page["text"])
