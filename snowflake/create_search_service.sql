-- Crée le Cortex Search Service sur la colonne "chunk"
CREATE OR REPLACE CORTEX SEARCH SERVICE document_processing_db.public.pdf_search_service
    ON chunk
    ATTRIBUTES language
    WAREHOUSE = document_processing_wh
    TARGET_LAG = '1 hour'
    AS (
        SELECT
            chunk,
            model_name,
            version,
            manufacturer,
            release_date
        FROM document_processing_db.public.chunked_pdf_documents
    );
