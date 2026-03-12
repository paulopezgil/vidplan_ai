import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://backend:8000")

st.set_page_config(page_title="TalentStream AI", layout="wide")
st.title("TalentStream AI")

tab_upload, tab_search = st.tabs(["Upload Employee", "Search Talent"])

# ── Upload tab ──────────────────────────────────────────────────────────────
with tab_upload:
    st.subheader("Add an Employee Profile")
    name = st.text_input("Name")
    title = st.text_input("Job Title")
    bio = st.text_area("Profile / Resume (free text)", height=200)
    col1, col2, col3 = st.columns(3)
    department = col1.text_input("Department")
    location = col2.text_input("Location")
    grade = col3.selectbox("Grade", [None, "junior", "mid", "senior", "lead"])

    if st.button("Upload"):
        if not name or not title or not bio:
            st.warning("Name, title, and profile text are required.")
        else:
            payload = {"name": name, "title": title, "bio": bio}
            if department:
                payload["department"] = department
            if location:
                payload["location"] = location
            if grade:
                payload["grade"] = grade
            resp = requests.post(
                f"{API_URL}/employees/upload",
                json=payload,
                timeout=30,
            )
            if resp.ok:
                data = resp.json()
                st.success(data.get("message", "Uploaded!"))
                st.json(data.get("parsed_profile", {}))
            else:
                st.error(f"Error {resp.status_code}: {resp.text}")

# ── Search tab ──────────────────────────────────────────────────────────────
with tab_search:
    st.subheader("Search for Talent")
    query = st.text_input("Describe the candidate you're looking for")
    top_k = st.slider("Results to return", 1, 20, 5)

    if st.button("Search"):
        if not query:
            st.warning("Please enter a search query.")
        else:
            resp = requests.post(
                f"{API_URL}/query",
                json={"query": query, "top_k": top_k},
                timeout=30,
            )
            if resp.ok:
                results = resp.json()
                if not results:
                    st.info("No matching candidates found.")
                for r in results:
                    with st.expander(f"{r['name']} — {r['title']} (score: {r['score']:.3f})"):
                        skills_display = ", ".join(
                            f"{s['name']} ({s.get('years_experience') or '?'}y)"
                            for s in r["skills"]
                        ) if r["skills"] else "N/A"
                        st.write(f"**Skills:** {skills_display}")
                        st.write(f"**Experience:** {r['years_experience']} years")
                        st.write(f"**Department:** {r.get('department', 'N/A')}")
                        st.write(f"**Grade:** {r.get('grade', 'N/A')}")
                        st.write(f"**Location:** {r['location']}")
                        st.write(f"**Bio:** {r['bio']}")
            else:
                st.error(f"Error {resp.status_code}: {resp.text}")
