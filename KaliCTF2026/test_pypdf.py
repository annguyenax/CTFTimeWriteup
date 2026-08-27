from pypdf import PdfReader

try:
    reader = PdfReader('skyline-parser/assets/reference/r03.pdf')
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print("PDF Text:")
    print(text)
except Exception as e:
    print(e)
