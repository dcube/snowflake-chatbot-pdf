-- Crée la base de données
CREATE DATABASE IF NOT EXISTS document_processing_db;

-- Crée un warehouse pour les traitements
CREATE OR REPLACE WAREHOUSE document_processing_wh
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 120
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

-- Active l’usage du warehouse
USE WAREHOUSE document_processing_wh;

-- Crée un stage pour uploader les fichiers PDF
CREATE OR REPLACE STAGE pdf_upload_stage
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Crée la table brute contenant les fichiers PDF
CREATE OR REPLACE TABLE document_processing_db.public.raw_pdf_documents (
    pdf_file STRING,
    model_name STRING,
    version STRING,
    manufacturer STRING,
    release_date STRING
);
