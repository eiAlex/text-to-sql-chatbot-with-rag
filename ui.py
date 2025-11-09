'''ui.py - Streamlit UI for the Text-to-SQL Chatbot with RAG application.'''

import logging
from typing import Any, Dict

import pandas as pd
import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
st.set_page_config(
    page_title="Text-to-SQL Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
div.stButton > button {
    border-radius: 12px;
    border: 2px solid transparent;
    font-weight: 600;
    font-size: 16px;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #ff4b4b, #ff6b6b);
    color: white;
    border: 2px solid #ff4b4b;
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #ff3333, #ff5555);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(255,75,75,0.3);
}

div.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    color: #475569;
    border: 2px solid #cbd5e1;
}

div.stButton > button[kind="secondary"]:hover {
    background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
    border-color: #94a3b8;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}


div[data-testid="column"]:nth-child(2) div.stButton > button {
    background: linear-gradient(135deg, #fef2f2, #fee2e2);
    color: #dc2626;
    border: 2px solid #fecaca;
}

div[data-testid="column"]:nth-child(2) div.stButton > button:hover {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    border-color: #f87171;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(220,38,38,0.2);
}
</style>
""", unsafe_allow_html=True)


def call_api(question: str, show_sql: bool = True) -> Dict[str, Any]:
    '''Call the Text-to-SQL API'''
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={
                "question": question,
                "show_sql": show_sql
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("API call error: %s", e)
        return {"success": False, "error": str(e)}


def check_api_health() -> bool:
    '''Check if the API is healthy'''
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def main():
    '''Main Streamlit UI function'''
    st.title("🤖 Text-to-SQL Chatbot")
    st.markdown(
        "### Ask questions in natural language and get database results")
    with st.sidebar:
        st.header("⚙️ Settings")
        if check_api_health():
            st.success("✅ API connected")
        else:
            st.error("❌ API unavailable")
            st.info(
                "Make sure the API is running on http://127.0.0.1:8000")
            return

        show_sql = st.checkbox("Show generated SQL", value=True)

        st.markdown("---")
        st.markdown("### 💡 Example questions:")
        st.markdown("""
        - How many sales were made?
        - What are the best-selling products?
        - List of active customers
        - Revenue by month
        """)
    col1, _ = st.columns([2, 1])

    with col1:
        question = st.text_area(
            "Type your question:",
            placeholder="Ex: How many sales were made in 2024?",
            height=100
        )

        col_btn1, col_btn2, _ = st.columns([1, 1, 4])

        with col_btn1:
            submit_button = st.button("🔍 Query", type="primary")

        with col_btn2:
            clear_button = st.button("🗑️ Clear", type="secondary")
    if submit_button and question.strip():
        with st.spinner("Processing query..."):
            result = call_api(question, show_sql)

            if result.get("success"):
                st.success("✅ Query executed successfully!")
                if show_sql and result.get("sql"):
                    st.subheader("📝 Generated SQL:")
                    st.code(result["sql"], language="sql")
                if result.get("rows"):
                    st.subheader("📊 Results:")
                    df = pd.DataFrame(result["rows"])
                    col_metric1, col_metric2 = st.columns(2)
                    with col_metric1:
                        st.metric("Total records", len(df))
                    with col_metric2:
                        st.metric("Columns", len(df.columns)
                                if not df.empty else 0)
                    st.dataframe(df, width='stretch')
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.info(
                        "ℹ️ Query executed, but no results were returned.")

            else:
                st.error(
                    f"❌ Query error: {result.get('error', 'Unknown error')}")

    elif submit_button and not question.strip():
        st.warning("⚠️ Please type a question.")

    if clear_button:
        st.rerun()
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    if submit_button and question.strip():
        if question not in [q["question"] for q in st.session_state.query_history]:
            st.session_state.query_history.append({
                "question": question,
                "timestamp": pd.Timestamp.now().strftime("%H:%M:%S")
            })
    with st.sidebar:
        if st.session_state.query_history:
            st.markdown("---")
            st.markdown("### 📝 History")
            for i, item in enumerate(reversed(st.session_state.query_history[-5:])):
                if st.button(f"{item['timestamp']}", key=f"hist_{i}"):
                    st.session_state.selected_question = item["question"]
                    st.rerun()


if __name__ == "__main__":
    main()
