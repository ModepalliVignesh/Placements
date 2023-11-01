from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import nltk
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("C:\\Users\\vigne\\Downloads\\tcs_questions_dataset_modified.csv")
questions_in_dataset = df["Questions"].tolist()

# Tokenize the dataset
tokens = []
for question in questions_in_dataset:
    tokens.extend(word_tokenize(question))

# Filter out unique nouns (as they are good candidates for generating questions)
nouns = [word for (word, pos) in nltk.pos_tag(tokens) if pos in ['NN', 'NNS', 'NNP', 'NNPS']]
unique_nouns = list(set(nouns))

# Basic question templates
templates = [
    "What is ___?",
    "How does ___ work?",
    "Why is ___ important?",
    "Can you explain ___?",
    "What do you know about ___?"
    "Explain ___."  
]

def generate_question():
    """Generate a question using a template and a noun from the dataset."""
    template = random.choice(templates)
    noun = random.choice(unique_nouns)
    question = template.replace("___", noun)
    return question
@app.route('/')
def home():
    return render_template('page1.html')

@app.route('/generate', methods=['POST'])
def generate_questions():
    generated_questions = set()

    while len(generated_questions) < 10:
        question = generate_question()
        if question not in questions_in_dataset:
            generated_questions.add(question)

    return jsonify({"questions": list(generated_questions)})

if __name__ == '__main__':
    app.run(debug=True)
