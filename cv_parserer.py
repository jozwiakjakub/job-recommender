import docx2txt
import PyPDF2
import io

def parse_cv(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    elif file_name.endswith(".docx"):
        # docx2txt potrzebuje ścieżki, więc zapisujemy do bufora
        with open("temp.docx", "wb") as f:
            f.write(uploaded_file.read())
        text = docx2txt.process("temp.docx")
        return text

    else:
        raise ValueError("Unsupported file format")