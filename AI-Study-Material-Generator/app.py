import streamlit as st
import PyPDF2
from generator import generate_summary, generate_keypoints, generate_quiz

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


st.set_page_config(
    page_title="AI Study Material Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Material Generator")

st.write(
"Upload a PDF or enter a topic to generate AI-powered study notes, key points, and quiz questions."
)

st.divider()


uploaded_file = st.file_uploader("Upload your study PDF", type="pdf")

topic = st.text_input("Or enter a topic")

text = ""


# Extract text from uploaded PDF safely
if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:   # prevents None errors
            text += page_text


# Use topic input
elif topic.strip() != "":
    text = topic



if st.button("Generate Study Material"):

    if text.strip() != "":

        with st.spinner("AI is generating study material..."):

            summary = generate_summary(text)
            keypoints = generate_keypoints(text)
            quiz = generate_quiz(text)

        st.subheader("📖 Summary")
        st.success(summary)

        st.subheader("📌 Key Points")
        st.info(keypoints)

        st.subheader("🧠 Quiz Questions")
        st.warning(quiz)


        def create_pdf(summary, keypoints, quiz):

            buffer = BytesIO()
            styles = getSampleStyleSheet()

            story = []

            story.append(Paragraph("AI Generated Study Notes", styles['Title']))
            story.append(Spacer(1,20))

            story.append(Paragraph("<b>Summary</b>", styles['Heading2']))
            story.append(Paragraph(summary, styles['BodyText']))
            story.append(Spacer(1,20))

            story.append(Paragraph("<b>Key Points</b>", styles['Heading2']))
            story.append(Paragraph(keypoints.replace("\n","<br/>"), styles['BodyText']))
            story.append(Spacer(1,20))

            story.append(Paragraph("<b>Quiz Questions</b>", styles['Heading2']))
            story.append(Paragraph(quiz.replace("\n","<br/>"), styles['BodyText']))

            doc = SimpleDocTemplate(buffer)
            doc.build(story)

            buffer.seek(0)

            return buffer


        pdf_file = create_pdf(summary, keypoints, quiz)

        st.download_button(
            label="📥 Download Study Notes PDF",
            data=pdf_file,
            file_name="study_notes.pdf",
            mime="application/pdf"
        )

    else:

        st.error("Please upload a PDF or enter a topic.")