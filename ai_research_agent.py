import streamlit as st
import requests

# 🔐 API Keys
SEARCH1_API_KEY = "C80C72AC-FB4C-45F7-9C3B-1C1F94E51DFB"
TEXTCORTEX_KEY = "gAAAAABoWHZhgckidemYJeJxWETgfB4zU8dJ_f7P5bu-mPQEhXqLcf3pVFPivL2-Mf1pyfBKMH3-M_vcVmxtSvovQDjxFFyOuhgwqZ3ynnwIu9RNIjzSQCakLl9ClyuGBag50CYg-OQfMK4q48kxq56tJuLsPpj-BXPQeRcfaiQFRe3mBaHHObE="

# ⚙️ Streamlit Page Config
st.set_page_config(page_title="Auto Researcher", layout="centered")
st.title("🔍 Auto Researcher")
st.markdown('<p style="text-align:center; font-size:26px;">What would you like to know?</p>', unsafe_allow_html=True)

try:
    # 📥 User Input
    query = st.text_input("", placeholder="Type your question here…")

    # 🔎 Search and Summarize
    if st.button("Research 🔎") and query:
        # Step 1: Search the Web
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

        # Step 2: Display Results
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

            # Step 3: Summarize the Combined Snippets
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
                                "length": "medium",  # can also be "short" or "long"
                                "language": "en"
                            }
                        )
                        summary_resp.raise_for_status()
                        summary = summary_resp.json().get("summary", "")
                    except Exception as e:
                        st.error(f"❌ Summarization failed: {e}")
                        st.stop()

                st.subheader("📝 Summary")
                st.write(summary or "No summary returned.")
                
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")