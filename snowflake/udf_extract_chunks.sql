CREATE OR REPLACE FUNCTION document_processing_db.public.extract_pdf_chunks(
    pdf_file STRING, model_name STRING, version STRING, manufacturer STRING, release_date STRING
)
    RETURNS TABLE (chunk STRING, model_name STRING, version STRING, manufacturer STRING, release_date STRING)
    LANGUAGE PYTHON
    RUNTIME_VERSION = '3.9'
    HANDLER = 'pdf_text_chunker'
    PACKAGES = ('snowflake-snowpark-python', 'langchain', 'pdfminer.six')
    AS
$$
from pdfminer.high_level import extract_text
import base64
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Optional

class pdf_text_chunker:

    def process(self, pdf_file: Optional[str], model_name: str, version: str, manufacturer: str, release_date: str):
        if pdf_file is None:
            return

        pdf_file_bytes = base64.b64decode(pdf_file)

        with open("/tmp/temp_pdf.pdf", "wb") as temp_pdf:
            temp_pdf.write(pdf_file_bytes)

        text = extract_text("/tmp/temp_pdf.pdf")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=300,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        for chunk in chunks:
            yield (chunk, model_name, version, manufacturer, release_date)
$$;
