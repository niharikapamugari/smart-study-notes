import spacy
from transformers import pipeline

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def generate_summary(text):
    """Generate long summary safely using chunking"""

    # Split text into chunks
    chunk_size = 900
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    summaries = []

    for chunk in text_chunks[:4]:  # limit chunks for speed
        result = summarizer(
            chunk,
            max_length=200,
            min_length=60,
            do_sample=False
        )

        summaries.append(result[0]["summary_text"])

    # Combine all chunk summaries
    final_summary = " ".join(summaries)

    return final_summary

def generate_keypoints(text):
    """Extract top 10 sentences as keypoints using spaCy"""

    doc = nlp(text)

    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text) > 20]

    keypoints = sentences[:10]

    formatted = ""

    for i, point in enumerate(keypoints):
        formatted += f"{i+1}. {point}\n"

    return formatted


def generate_quiz(text):
    """Generate quiz using nouns from sentences"""

    doc = nlp(text)

    sentences = list(doc.sents)[:10]

    quiz = ""

    q_num = 1

    for sent in sentences:

        target_token = None

        for token in sent:

            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
                target_token = token
                break

        if target_token:

            answer = target_token.text

            question = sent.text.replace(answer, "_______", 1)

            quiz += f"Q{q_num}: {question.strip()}\n"
            quiz += f"Answer: {answer}\n\n"

            q_num += 1

    return quiz