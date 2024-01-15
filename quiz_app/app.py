from flask import Flask, render_template, request, flash, redirect, url_for
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load datasets
with open('dataset1.json') as f:
    dataset1 = json.load(f)

with open('dataset2.json') as f:
    dataset2 = json.load(f)

# Combine datasets
combined_dataset = {**dataset1, **dataset2}

@app.route('/')
def index():
    # Choose a random passage
    passage_id, passage_data = random.choice(list(combined_dataset.items()))
    passage = passage_data['passage']
    questions = passage_data['qa_pairs']
    return render_template('index.html', passage_id=passage_id, passage=passage, questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    passage_id = request.form['passage_id']
    user_answers = {}
    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = key.replace('question_', '')
            user_answers[question_id] = value

    # Check answers
    correct_answers = combined_dataset[passage_id]['qa_pairs']
    score = 0
    correct_questions = []
    wrong_questions = []

    for question_id, user_answer in user_answers.items():
        correct_answer_found = False
        for q in correct_answers:
            if q['query_id'] == question_id:
                spans = q['answer']['spans']
                for span in spans:
                    if user_answer.lower() in span.lower():
                        correct_answer_found = True
                        score += 1
                        break

        if correct_answer_found:
            correct_questions.append(question_id)
        else:
            wrong_questions.append(question_id)

    # Redirect to the results page
    return redirect(url_for('results', score=score, correct_questions=correct_questions, wrong_questions=wrong_questions))

@app.route('/results')
def results():
    score = request.args.get('score', type=int, default=0)
    correct_questions = request.args.getlist('correct_questions')
    wrong_questions = request.args.getlist('wrong_questions')

    return render_template('results.html', score=score, correct_questions=correct_questions, wrong_questions=wrong_questions)

if __name__ == '__main__':
    app.run(debug=True)
