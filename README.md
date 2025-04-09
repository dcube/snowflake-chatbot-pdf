# ❄️ Snowflake PDF Chatbot

Créez un chatbot intelligent capable de répondre à des questions basées sur le contenu de documents PDF, grâce à **Snowflake Cortex Search** et **Streamlit**.  
Ce projet démontre comment extraire du texte de fichiers PDF, l’indexer dans Snowflake, et interagir avec les données via une interface utilisateur moderne.

---

## 🚀 Fonctionnalités

- 📄 Extraction automatique de texte à partir de fichiers PDF via UDF Python
- 🧠 Chunking intelligent du contenu avec `langchain`
- 🔎 Recherche sémantique performante avec **Snowflake Cortex Search**
- 💬 Interface conversationnelle interactive avec **Streamlit**
- 🔗 Référencement des documents PDF dans les réponses du chatbot

---

## 📦 Architecture du projet

```bash
snowflake-chatbot-pdf/
├── README.md
├── snowflake/
│   ├── create_objects.sql            # Création de la DB, warehouse, stage
│   ├── udf_extract_chunks.sql        # UDF Python pour extraire et découper les PDF
│   ├── ingest_chunks.sql             # Ingestion des PDF dans la table d'analyse
│   └── create_search_service.sql     # Déploiement du service Cortex Search
│
├── streamlit_app/
│   └── app.py                        # Interface utilisateur du chatbot
│
└── requirements.txt                  # Dépendances Python (optionnel)


## 🧱 Setup Snowflake

Exécute les scripts SQL dans l’ordre suivant : 

-- 1. Créer la DB, le warehouse, et le stage
snowflake/create_objects.sql

-- 2. Déployer l'UDF pour découper les PDF
snowflake/udf_extract_chunks.sql

-- 3. Créer les tables et ingérer les chunks
snowflake/ingest_chunks.sql

-- 4. Créer le service de recherche Cortex
snowflake/create_search_service.sql

Uploade tes fichiers PDF dans le stage :

Interface Snowflake (Snowsight) → Data → pdf_upload_stage → Upload

## 💬 Lancer l'application Chatbot

streamlit run app.py

