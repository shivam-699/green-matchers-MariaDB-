import streamlit as st
import requests
import json




st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then(() => console.log('Service Worker registered'))
      .catch(err => console.log('Service Worker error:', err));
  }
</script>
""", unsafe_allow_html=True)



st.title("Green Matchers: Revolutionozing Eco Jobs with AI")

skill = st.text_input("Enter your skills (e.g., Python, Django):")
if st.button("Find Matches & Stories"):
    if skill:
        try:
            # Call match endpoint
            match_response = requests.post("http://127.0.0.1:8000/match_jobs", json={"skill_text": skill})
            matches = match_response.json()
            st.subheader("Top Job Matches:")
            for match in matches:
                st.write(f"**{match['job_title']}** (Similarity: {match['similarity']:.2f})")
                st.write(match['description'])

            # Call narrative endpoint
            narrative_response = requests.post("http://127.0.0.1:8000/generate_narrative", json={"skill_text": skill})
            narrative = narrative_response.json()["narrative"]
            st.subheader("Personalized Story:")
            st.write(narrative)
        except Exception as e:
            st.error(f"Error: {str(e)} - Make sure backend server is running!")
    else:
        st.warning("Enter skills first!")







# Run Frontend: New terminal (or stop backend temporarily) > streamlit run frontend.py

# Opens browser (e.g., http://localhost:8501). Test: Enter skills > Button > Shows matches + story.
# Note: Backend must be running in another terminal for API calls.