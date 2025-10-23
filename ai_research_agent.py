import streamlit as st
import requests
import os

# 🔐 API Keys
SEARCH1_API_KEY = os.getenv("SEARCH1_API_KEY")
TEXTCORTEX_KEY = os.getenv("TEXTCORTEX_KEY")
if not SEARCH1_API_KEY or not TEXTCORTEX_KEY:
    st.error("⚠️ Missing API keys. Please set them in Streamlit Secrets.")
    st.stop()

# ⚙️ Streamlit Page Config
st.set_page_config(page_title="Auto Researcher", layout="centered")
st.title("🔍 Auto Researcher")
st.markdown('<p style="text-align:center; font-size:26px;">What would you like to know?</p>', unsafe_allow_html=True)

try:
    query = st.text_input("", placeholder="Type your question here…")

    if st.button("Research 🔎") and query:
        with st.spinner("🔍 Searching the internet..."):
            try:
                search_resp = requests.post(
                    "https://api.search1api.com/search",
                    headers={"Authorization": f"Bearer {SEARCH1_API_KEY}"},
                    json={"query": query, "search_service": "google", "max_results": 5}
                )
                search_resp.raise_for_status()
            except Exception as e:
                st.error(f"❌ Search failed: {e}")
                st.stop()

        results = search_resp.json().get("results", [])
        snippets = []

        if not results:
            st.warning("⚠️ No results found.")
        else:
            st.subheader("🌐 Top Results")
            for result in results:
                title = result.get("title", "No title")
                url = result.get("url", "#")
                snippet = result.get("snippet", "No snippet available.")
                
                st.markdown(f"**{title}** — [View Source]({url})")
                st.write(snippet)
                snippets.append(snippet)

            combined_text = " ".join(snippets).strip()

            if not combined_text:
                st.warning("⚠️ Not enough content to summarize.")
            else:
                with st.spinner("🧠 Summarizing with TextCortex..."):
                    try:
                        summary_resp = requests.post(
                            "https://api.textcortex.com/v1/texts/summarize",
                            headers={
                                "Authorization": f"Bearer {TEXTCORTEX_KEY}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "text": combined_text,
                                "length": "medium",
                                "language": "en"
                            }
                        )
                        summary_resp.raise_for_status()
                        data = summary_resp.json()
                        summary = data.get("data", [{}])[0].get("text", "")
                    except Exception as e:
                        st.error(f"❌ Summarization failed: {e}")
                        st.stop()

                st.subheader("📝 Summary")
                st.write(summary or "No summary returned.")

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
