from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline


MODEL_NAME = 'distilbert-base-uncased-distilled-squad'
HANDBOOK_PATH = 'path/to/your/handbook.txt'

def read_handbook_paragraphs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        paragraphs = [para.strip() for para in text.split('\n\n') if para.strip() != '']
    return paragraphs

def find_relevant_paragraph(question, paragraphs):
    vectorizer = TfidfVectorizer().fit(paragraphs)
    question_vec = vectorizer.transform([question])
    paragraphs_vec = vectorizer.transform(paragraphs)
    similarities = cosine_similarity(question_vec, paragraphs_vec)
    most_relevant_idx = similarities.argmax()
    return paragraphs[most_relevant_idx], similarities[0, most_relevant_idx]

def get_answer(question, context):
    qa_pipeline = pipeline("question-answering", model=MODEL_NAME, tokenizer=MODEL_NAME)
    return qa_pipeline({'context': context, 'question': question})['answer']

def main():
    question = "What are the main safety guidelines?"
    handbook_paragraphs = read_handbook_paragraphs(HANDBOOK_PATH)
    relevant_paragraph, similarity_score = find_relevant_paragraph(question, handbook_paragraphs)
    
    answer = get_answer(question, relevant_paragraph)
    print(f"Question: {question}")
    print(f"Most relevant paragraph: {relevant_paragraph}")
    print(f"Similarity score: {similarity_score}")
    print(f"Answer: {answer}")

if __name__ == '__main__':
    main()
