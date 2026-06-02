import streamlit as st
import PyPDF2
import docx
from fpdf import FPDF
import tempfile

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Meeting Minutes Summarizer",
    page_icon="📝",
    layout="wide"
)

# ==========================
# TITLE
# ==========================

st.title("📝 AI Meeting Minutes Summarizer")

st.markdown("---")

# ==========================
# SUMMARY FUNCTION
# ==========================

def generate_summary(text):

    sentences = text.split('.')

    summary = '. '.join(sentences[:3])

    return summary.strip()

# ==========================
# PDF READER
# ==========================

def read_pdf(uploaded_file):

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() + " "

    return text

# ==========================
# DOCX READER
# ==========================

def read_docx(uploaded_file):

    doc = docx.Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + " "

    return text

# ==========================
# PDF DOWNLOAD
# ==========================

def create_pdf(summary_text):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(
        0,
        10,
        summary_text
    )

    pdf_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    pdf.output(pdf_file.name)

    return pdf_file.name

# ==========================
# SECTION 1
# ==========================

st.subheader("Section 1: Enter Meeting Notes")

meeting_notes = st.text_area(
    "Paste meeting notes here...",
    height=250
)

# ==========================
# BONUS 1 PDF
# ==========================

pdf_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if pdf_file:

    meeting_notes = read_pdf(pdf_file)

    st.success("PDF Uploaded Successfully")

# ==========================
# BONUS 2 DOCX
# ==========================

docx_file = st.file_uploader(
    "Upload DOCX",
    type=["docx"]
)

if docx_file:

    meeting_notes = read_docx(docx_file)

    st.success("DOCX Uploaded Successfully")

# ==========================
# SECTION 2
# ==========================

st.subheader("Section 2: Generate Summary")

if st.button("Generate Summary"):

    if meeting_notes.strip() == "":

        st.warning("Please enter meeting notes.")

    else:

        summary = generate_summary(
            meeting_notes
        )

        # ==========================
        # SECTION 3
        # ==========================

        st.subheader(
            "Section 3: AI Generated Summary"
        )

        st.success(summary)

        # ==========================
        # SECTION 4
        # ==========================

        original_words = len(
            meeting_notes.split()
        )

        summary_words = len(
            summary.split()
        )

        compression_ratio = (
            (original_words - summary_words)
            / original_words
        ) * 100

        st.subheader("Section 4: Statistics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Original Words",
            original_words
        )

        col2.metric(
            "Summary Words",
            summary_words
        )

        col3.metric(
            "Compression Ratio",
            f"{compression_ratio:.2f}%"
        )

        # ==========================
        # BONUS 3
        # ==========================

        pdf_path = create_pdf(summary)

        with open(pdf_path, "rb") as file:

            st.download_button(
                label="📥 Download Summary as PDF",
                data=file,
                file_name="meeting_summary.pdf",
                mime="application/pdf"
            )
