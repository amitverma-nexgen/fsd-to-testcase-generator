import streamlit as st
import pandas as pd
import uuid
from docx import Document
from io import BytesIO

# --- Read the uploaded .docx file and extract text ---
def read_docx(uploaded_file):
    doc = Document(uploaded_file)
    full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return full_text

# --- Rule-based test case generator ---
def generate_test_cases(fsd_text):
    cases = []

    if "Timer to be displayed" in fsd_text:
        cases.append({
            "Test Case ID": str(uuid.uuid4())[:8],
            "Title": "Display LIVE event timer in hours/minutes if within 24 hours",
            "Steps": "1. Set upcoming event time within 24 hrs\n2. Launch app\n3. Navigate to banner",
            "Expected Result": "Timer shows hours and minutes"
        })
        cases.append({
            "Test Case ID": str(uuid.uuid4())[:8],
            "Title": "Display LIVE event date if more than 24 hours away",
            "Steps": "1. Set upcoming event time to >24 hrs\n2. Launch app\n3. Navigate to banner",
            "Expected Result": "Timer shows the event date"
        })

    if "Buy Tickets link" in fsd_text:
        cases.append({
            "Test Case ID": str(uuid.uuid4())[:8],
            "Title": "Validate Buy Tickets link is dynamic",
            "Steps": "1. Launch app with Event A\n2. Note 'Buy Tickets' link\n3. Switch to Event B\n4. Verify updated link",
            "Expected Result": "'Buy Tickets' link updates per event"
        })

    if "How to Watch" in fsd_text:
        cases.append({
            "Test Case ID": str(uuid.uuid4())[:8],
            "Title": "How to Watch CTA opens in new web view on mobile",
            "Steps": "1. Launch mobile app\n2. Tap 'How to Watch' CTA",
            "Expected Result": "New web view opens with event info"
        })

    return cases

# --- Streamlit UI ---
st.set_page_config(page_title="FSD to Test Case Generator", layout="centered")
st.title("📄 FSD to Test Case Generator")
st.markdown("Upload your `.docx` Functional Spec and download generated test cases as `.xls`.")

uploaded_file = st.file_uploader("Upload FSD (.docx only)", type=["docx"])

if uploaded_file:
    with st.spinner("Reading and analyzing FSD..."):
        fsd_text = read_docx(uploaded_file)
        test_cases = generate_test_cases(fsd_text)

        if test_cases:
            df = pd.DataFrame(test_cases)

            # Display preview
            st.success("✅ Test cases generated!")
            st.dataframe(df, use_container_width=True)

            # Excel export
            output = BytesIO()
            df.to_excel(output, index=False, engine='xlwt')
            output.seek(0)

            st.download_button(
                label="📥 Download Test Cases (.xls)",
                data=output,
                file_name="generated_test_cases.xls",
                mime="application/vnd.ms-excel"
            )
        else:
            st.warning("No test cases could be generated. Make sure your FSD has valid content.")
