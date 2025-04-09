import streamlit as st
from snowflake.core import Root
from snowflake.cortex import Complete
from snowflake.snowpark.context import get_active_session

AVAILABLE_MODELS = [
    "mistral-large2",
    "llama3.1-70b",
    "llama3.1-8b",
]

def initialize_messages():
    if st.session_state.get("clear_conversation", False) or "messages" not in st.session_state:
        st.session_state.messages = []

def load_service_metadata():
    if "service_metadata" not in st.session_state:
        services = session.sql("SHOW CORTEX SEARCH SERVICES;").collect()
        metadata = []
        for s in services:
            name = s["name"]
            desc = session.sql(f"DESC CORTEX SEARCH SERVICE {name};").collect()
            column = desc[0]["search_column"]
            metadata.append({"name": name, "search_column": column})
        st.session_state.service_metadata = metadata

def sidebar_config():
    service_names = [s["name"] for s in st.session_state.service_metadata]
    st.sidebar.selectbox("Search Service", service_names, key="selected_cortex_search_service")

    st.sidebar.button("Clear Conversation", key="clear_conversation")
    st.sidebar.toggle("Debug", key="debug", value=False)
    st.sidebar.toggle("Use Chat History", key="use_chat_history", value=True)

    with st.sidebar.expander("Advanced Settings"):
        st.selectbox("Model", AVAILABLE_MODELS, key="model_name")
        st.number_input("Context Chunks", 1, 10, 5, key="num_retrieved_chunks")
        st.number_input("Chat History Length", 1, 10, 5, key="num_chat_messages")

    st.sidebar.expander("Session State").write(st.session_state)

def query_service(user_input, columns=None, filters=None):
    columns = columns or []
    filters = filters or {}

    db, schema = session.get_current_database(), session.get_current_schema()
    service = root.databases[db].schemas[schema].cortex_search_services[
        st.session_state.selected_cortex_search_service
    ]

    results = service.search(user_input, columns=columns, filter=filters, limit=st.session_state.num_retrieved_chunks).results
    column_name = next(s["search_column"] for s in st.session_state.service_metadata if s["name"] == st.session_state.selected_cortex_search_service).lower()

    context = "\n".join(f"Context {i + 1}: {r[column_name]}" for i, r in enumerate(results))

    if st.session_state.debug:
        st.sidebar.text_area("Context Results", context, height=500)

    return context, results

def get_recent_messages():
    history = st.session_state.messages
    return history[-st.session_state.num_chat_messages:-1] if history else []

def generate_completion(model, prompt):
    return Complete(model, prompt).replace("$", "\$")

def summarize_history(history, question):
    prompt = f"""
    [INST]
    Extend the question below using the given chat history. Return only the extended query.
    <chat_history>
    {history}
    </chat_history>
    <question>
    {question}
    </question>
    [/INST]
    """
    summary = generate_completion(st.session_state.model_name, prompt)

    if st.session_state.debug:
        st.sidebar.text_area("Extended Query", summary, height=150)

    return summary

def build_prompt(question):
    chat_history = get_recent_messages() if st.session_state.use_chat_history else []
    query = summarize_history(chat_history, question) if chat_history else question

    context, results = query_service(
        query,
        columns=["chunk", "model_name", "version"],
        filters={"@and": [{"@eq": {"language": "English"}}]},
    )

    formatted_history = "\n".join(msg["content"] for msg in chat_history) if chat_history else ""

    prompt = f"""
    [INST]
    You are a helpful AI assistant using retrieved documents and previous conversation context.
    Use the provided context and history to answer the question accurately.

    <chat_history>
    {formatted_history}
    </chat_history>
    <context>
    {context}
    </context>
    <question>
    {question}
    </question>
    [/INST]
    Answer:
    """

    return prompt, results

def main():
    st.title(":speech_balloon: PDF Search ChatBot")

    load_service_metadata()
    sidebar_config()
    initialize_messages()

    avatars = {"user": "👤", "assistant": "❄️"}

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=avatars[msg["role"]]):
            st.markdown(msg["content"])

    if not st.session_state.service_metadata:
        st.warning("No Cortex search services found.")
        return

    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=avatars["user"]):
            st.markdown(user_input.replace("$", "\$"))

        with st.chat_message("assistant", avatar=avatars["assistant"]):
            with st.spinner("Thinking..."):
                prompt, refs = build_prompt(user_input)
                response = generate_completion(st.session_state.model_name, prompt)

                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    session = get_active_session()
    root = Root(session)
    main()
