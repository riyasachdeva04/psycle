import json
import os
import random
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from forms import LoginForm, RegistrationForm
from test_form import AutismForm
from patient_bot.main import load_quotes, get_most_apt_quote

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/test', methods=['GET', 'POST'])
def autism_form():
    form = AutismForm()

    if request.method == 'POST' and form.validate_on_submit():
        print("Social_Responsiveness_Scale:", form.Social_Responsiveness_Scale.data)
        print("Age_Years:", form.Age_Years.data)
        print("Qchat_10_Score:", form.Qchat_10_Score.data)
        print("Speech_Delay_Language_Disorder:", form.Speech_Delay_Language_Disorder.data)
        print("Learning_Disorder:", form.Learning_Disorder.data)
        print("Genetic_Disorders:", form.Genetic_Disorders.data)
        print("Depression:", form.Depression.data)
        print("Global_Developmental_Delay:", form.Global_Developmental_Delay.data)
        print("Social_Behavioural_Issues:", form.Social_Behavioural_Issues.data)
        print("Childhood_Autism_Rating_Scale:", form.Childhood_Autism_Rating_Scale.data)
        print("Sex:", form.Sex.data)
        print("Family_mem_with_ASD:", form.Family_mem_with_ASD.data)
        print("A10_score:", form.A10_score.data)

        prediction = form.predict()

        print(f'Model Prediction: {prediction}', 'info')
        return redirect(url_for('autism_form')) 
    return render_template('test.html', form=form)

@app.route('/grow')  
@app.route('/grow/dashboard')  
def grow_dashboard():
    squaresList = []
    return render_template('grow/dashboard.html', squaresList=squaresList)

@app.route('/grow/badges')
def grow_badges():
    return render_template('grow/badges.html')

@app.route('/grow/analytics')
def grow_analytics():
    return render_template('grow/analytics.html')

with open('dataset1.json') as f:
    dataset1 = json.load(f)

with open('dataset2.json') as f:
    dataset2 = json.load(f)

combined_dataset = {**dataset1, **dataset2}

@app.route('/quiz')
def quiz():
    # Choose a random passage
    passage_id, passage_data = random.choice(list(combined_dataset.items()))
    passage = passage_data['passage']
    questions = passage_data['qa_pairs']
    return render_template('quiz/index.html', passage_id=passage_id, passage=passage, questions=questions)

@app.route('/quiz/submit', methods=['POST'])
def submit():
    passage_id = request.form['passage_id']
    user_answers = {}
    for key, value in request.form.items():
        if key.startswith('question_'):
            question_id = key.replace('question_', '')
            user_answers[question_id] = value

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

    # Store information in session
    session['quiz_results'] = {
        'passage_id': passage_id,
        'user_answers': user_answers,
        'score': score,
        'correct_questions': correct_questions,
        'wrong_questions': wrong_questions
    }

    return render_template('quiz/submit.html', passage_id=passage_id, user_answers=user_answers)

@app.route('/quiz/results')
def results():
    quiz_results = session.get('quiz_results', {})
    return render_template('quiz/results.html', quiz_results=quiz_results)

chat_messages = []
@app.route('/helpbot/patient', methods=['GET', 'POST'])
def patient_bot():

    if request.method == 'POST':
        user_input = request.form['user_input']

        if user_input:
            quotes_data = load_quotes()
            most_apt_quote = get_most_apt_quote(user_input, quotes_data)

            # Append the initial bot message and user input to chat_messages
            chat_messages.append({'type': 'user', 'content': user_input})

            # Append the bot reply to chat_messages
            chat_messages.append({'type': 'bot', 'content': most_apt_quote['text']})

            return render_template('helpbot/patient.html', chat_messages=chat_messages, user_input=user_input, quote=most_apt_quote['text'])

    return render_template('helpbot/patient.html', chat_messages=chat_messages)

@app.route('/helpbot/parent')
def parent_bot():
    return render_template('helpbot/parent.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)