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

