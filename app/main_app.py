import json
import os
import random
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from forms import LoginForm, RegistrationForm
from test_form import AutismForm
from patient_bot.main import load_quotes, get_most_apt_quote
from parent_bot.botapp import get_response
from flask_socketio import SocketIO , emit
import base64
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import subprocess
cmd = 'python3 ./grow_dashboard/cv/main.py'


app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/openScript',  methods=['GET'])
def openScript():
    print('Opening Script')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate() 
    result = out.split('\n')
    for lin in result:
        if not lin.startswith('#'):
            print(lin)

@app.route('/test', methods=['GET', 'POST'])
def autism_form():
    form = AutismForm()
    if request.method == 'POST' and form.validate_on_submit():
        prediction = form.predict()
        dict = {1: 'Likely Autistic', 0: 'Unlikely to be Autistic'}
        alert_message = f'Model Prediction: {dict[prediction]}'
        return render_template('test.html', form=form, alert_message=alert_message)
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

chat_messages2 = []

@app.route('/parent-bot', methods=['GET', 'POST'])  
def parent_bot():
    user_input = ""
    response = ""
    if request.method == 'POST':
    
        user_input = request.form['user_input']

        response = get_response(user_input)

        chat_messages2.append({'type': 'user', 'content': user_input})
        chat_messages2.append({'type': 'bot', 'content': response})

    return render_template('helpbot/parent.html', chat_messages=chat_messages2, user_input=user_input, response=response)

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

count = 0
# websocket wala code 

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('video_frame')
# def handle_video_frame(frame):
#     # print('\n \n ', frame , '\n')
#     # im_bytes = base64.b64decode(frame)
#     # im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
#     # nparr = np.fromstring(frame, np.uint8)
#     # img = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)
#     frame = frame.split(',')[1]
#     image_data = base64.b64decode(frame)
#     image = Image.open(BytesIO(image_data))
#     # img = cv2.imageDecoder(frame, cv2.IMREAD_COLOR)
#     # print('\n \n ', img.dtype , '\n')
#     # print('\n \n ', image , '\n')
#     image_np = np.array(image)
#     grayFrame = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#     new = predict(image_np)
#     # _, im_arr = cv2.imencode('.jpg', grayFrame)  # im_arr: image in Numpy one-dim array format.
#     _, im_arr = cv2.imencode('.jpg', grayFrame)
#     im_bytes = im_arr.tobytes()
#     im_b64 = base64.b64encode(im_bytes)
#     #some procesiing 
#     # print('\n \n ', im_b64 , '\n')
#     base64_string = im_b64.decode('utf-8')  # Convert bytes to string

# # Prepend with data URL scheme information
#     img_str = "data:image/jpeg;base64," + base64_string

#     emit('processed' , img_str)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
