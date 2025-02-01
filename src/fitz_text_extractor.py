from io import BytesIO
import fitz
from docx2txt import process
import io
from src.helper_function import return_exception,clean_docx_file

def load_file(input_file):
    file_content = input_file.file.read()
    file = fitz.open(stream=BytesIO(file_content),filetype='pdf')
    return file


def extract_text(input_file):
    try:
        if input_file.filename.endswith(".docx"):
            text = process(io.BytesIO(input_file.file.read()))
            processed_text = clean_docx_file(text)
            return processed_text
        elif input_file.filename.endswith(".pdf"):
            input_doc = load_file(input_file)
            output_text = ''
            for page_num in range(input_doc.page_count):
                page = input_doc.load_page(page_num)
                output_text += page.get_text('text')
            return output_text
        else:
            return return_exception("Invalid input resume format")
        
    except Exception as e:
        return return_exception(e)