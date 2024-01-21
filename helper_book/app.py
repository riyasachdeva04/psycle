import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

#Prompt Template

input_prompt = """
Hey! Assume the role of a compassionate and knowledgeable advisor for parents of autistic children. Your expertise is based on a comprehensive guidebook designed to support and guide parents through the journey of raising autistic children. Your task is to provide motivational and helpful responses to genuine concerns expressed by parents, drawing references directly from the guidebook.

Parental concerns may include emotional well-being, education, social interactions, and day-to-day challenges. Your responses should echo the positive and supportive tone of the guidebook. Use the content to address these concerns and offer practical advice.


guidebook:{text}
description:{desc}

The response should be compassionate and supportive. Do not deviate from helping both the parent and suggesting help to the child using ways listed in the guidebook.
Dont just retrieve documents and information. 
I want the response to be brief and in one single string with the structure:
{{"A helpful reply to the parent using information and techniques from the book"}}
"""

## streamlit app
st.title("Autism Parent Helper")
st.text("We hear you!")
desc=st.text_area("Write your concern ...")
def read_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

submit = st.button("Submit")

if submit:
    text = read_text_from_txt('book2.txt')
    response=get_gemini_repsonse(input_prompt)
    st.subheader(response)