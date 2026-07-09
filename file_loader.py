from io import BytesIO


def _read_pdf(data:bytes)->str:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise ValueError(
            "PDF support requires the pypdf package. Install it with `pip install pypdf`."
        ) from exc

    reader = PdfReader(BytesIO(data))
    # pypdf's PageObject provides `extract_text()` (older code used
    # `extracted_text()` which isn't available on some versions).
    texts = []
    for page in reader.pages:
        # `extract_text()` can return None for empty pages.
        piece = page.extract_text()
        texts.append(piece or "")
    return "\n".join(texts)


def _read_docx(data:bytes)->str:
    try:
        from docx import Document
    except ModuleNotFoundError as exc:
        raise ValueError(
            "DOCX support requires the python-docx package. Install it with `pip install python-docx`."
        ) from exc

    doc = Document(BytesIO(data))
    return "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    )
def _read_txt(data:bytes)->str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1",errors="ignore")
    
def load_text(filename:str ,data:bytes)->str:

    name = filename.lower()

    if name.endswith(".txt"):
        text = _read_txt(data)
    elif name.endswith(".pdf"):
        text = _read_pdf(data)
    elif name.endswith(".docx"):
        text = _read_docx(data)
    else:
        raise ValueError(f"Unsupported file type :{filename}")
    
    if not text.strip():
        raise ValueError(
            f"No readable text found in {filename}"
            "If it's a scanned PDF, it has no selectable text to extract."
        )
    return text


if __name__=="__main__":
    demo = load_text("demo.txt", b"Chroma stores vectors. RAG retrieves them.")
    print("load_text() returned:", repr(demo))