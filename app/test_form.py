from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, RadioField
from wtforms.validators import InputRequired, NumberRange, AnyOf
import pickle
import numpy as np


class AutismForm(FlaskForm):
    Social_Responsiveness_Scale = IntegerField('Social Responsiveness Scale', validators=[NumberRange(min=1, max=10), InputRequired()])
    Age_Years = IntegerField('Age (Years)', validators=[InputRequired()])
    Qchat_10_Score = IntegerField('Qchat 10 Score', validators=[NumberRange(min=1, max=10), InputRequired()])
    Speech_Delay_Language_Disorder = SelectField('Speech Delay/Language Disorder', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Learning_Disorder = SelectField('Learning Disorder', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Genetic_Disorders = SelectField('Genetic Disorders', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Depression = SelectField('Depression', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Global_Developmental_Delay = SelectField('Global Developmental Delay/Intellectual Disability', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Social_Behavioural_Issues = SelectField('Social/Behavioural Issues', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Childhood_Autism_Rating_Scale = IntegerField('Childhood Autism Rating Scale', validators=[NumberRange(min=1, max=10), InputRequired()])
    Sex = RadioField('Sex', choices=[('M', 'Male'), ('F', 'Female')], validators=[AnyOf(['M', 'F']), InputRequired()])
    Family_mem_with_ASD = SelectField('Family member with ASD', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    A10_score = IntegerField('A10-score', validators=[NumberRange(min=1, max=10), InputRequired()])

    

    def predict(self):

        input_data = {
            'Social_Responsiveness_Scale': self.Social_Responsiveness_Scale.data,
            'Age_Years': self.Age_Years.data, 
            'Qchat_10_Score': self.Qchat_10_Score.data,
            'Speech_Delay_Language_Disorder': 1 if self.Speech_Delay_Language_Disorder.data == 'Yes' else 0,
            'Learning_Disorder': 1 if self.Learning_Disorder.data == 'Yes' else 0,
            'Genetic_Disorders': 1 if self.Genetic_Disorders.data == 'Yes' else 0,
            'Depression': 1 if self.Depression.data == 'Yes' else 0,
            'Global_Developmental_Delay': 1 if self.Global_Developmental_Delay.data == 'Yes' else 0,  
            'Social_Behavioural_Issues': 1 if self.Social_Behavioural_Issues.data == 'Yes' else 0, 
            
            'Childhood_Autism_Rating_Scale': self.Childhood_Autism_Rating_Scale.data,   
            'Sex': 1 if self.Sex.data == 'M' else 0,
            'Family_mem_with_ASD': 1 if self.Family_mem_with_ASD.data == 'Yes' else 0,
            'A10_score': self.A10_score.data
        }

        with open('prediction/rfc.pkl', 'rb') as file:
            model = pickle.load(file)["model"]

        input_array = np.array([list(input_data.values())], dtype="float32") 
        
        y_pred = model.predict(input_array)

        return y_pred[0]
