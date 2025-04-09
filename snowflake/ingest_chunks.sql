-- Crée une table pour stocker les chunks extraits
CREATE OR REPLACE TABLE document_processing_db.public.chunked_pdf_documents AS
SELECT
    t.chunk,
    t.model_name,
    t.version,
    t.manufacturer,
    t.release_date
FROM document_processing_db.public.raw_pdf_documents raw,
     TABLE(document_processing_db.public.extract_pdf_chunks(
         raw.pdf_file, raw.model_name, raw.version, raw.manufacturer, raw.release_date
     )) t;
