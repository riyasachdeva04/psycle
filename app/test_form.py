from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField
from wtforms.validators import InputRequired

class AutismForm(FlaskForm):
    Social_Responsiveness_Scale = RadioField('Social Responsiveness Scale', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Age_Years = RadioField('Age (Years)', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Qchat_10_Score = RadioField('Qchat 10 Score', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Speech_Delay_Language_Disorder = RadioField('Speech Delay/Language Disorder', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Learning_Disorder = RadioField('Learning Disorder', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Genetic_Disorders = RadioField('Genetic Disorders', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Depression = RadioField('Depression', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Global_Developmental_Delay = RadioField('Global Developmental Delay/Intellectual Disability', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Social_Behavioural_Issues = RadioField('Social/Behavioural Issues', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Childhood_Autism_Rating_Scale = RadioField('Childhood Autism Rating Scale', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Sex = RadioField('Sex', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    Ethnicity = SelectField('Ethnicity', choices=[('Indian', 'Indian'), ('Australian', 'Australian'), ('Canadian', 'Canadian')], validators=[InputRequired()])
    Family_mem_with_ASD = RadioField('Family member with ASD', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    A10_score = RadioField('A10-score', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])


