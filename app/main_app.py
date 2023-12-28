from curses import flash
from flask import Flask, redirect, render_template, request, url_for
from forms import LoginForm, RegistrationForm
from test_form import AutismForm
# from forms import RegistrationForm

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
        print("Ethnicity:", form.Ethnicity.data)

    return render_template('test.html', form=form)

@app.route('/grow')
def grow():
    return render_template('grow/dashboard.html')

@app.route('/grow/dashboard')
def grow_dashboard():
    return render_template('grow/dashboard.html')

@app.route('/grow/courses')
def grow_courses():
    return render_template('grow/courses.html')

@app.route('/grow/analytics')
def grow_analytics():
    return render_template('grow/analytics.html')

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