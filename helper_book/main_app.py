from flask import Flask, render_template, request
import os
import google.generativeai as genai

app = Flask(__name__)

# Load model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  
model = genai.GenerativeModel('gemini-pro')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=['POST'])
def get_response():
    concern = request.form['concern']  
    response = generate_response(concern)
    return response

def generate_response(concern):
    # Construct prompt using concern
    prompt = """
    Parent's concern: {concern}
    Your compassionate response including advice from the guidebook:
    """

    prompt = prompt.format(concern=concern)
    
    # Get Gemini response
    ans = model.generate_content(prompt)
    return ans.text

if __name__ == "__main__":
    app.run()