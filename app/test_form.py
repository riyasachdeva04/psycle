from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, RadioField
from wtforms.validators import InputRequired, NumberRange, AnyOf

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
    Ethnicity = SelectField('Ethnicity', choices=[
        ('Asian', 'Asian'),
        ('White European', 'White European'),
        ('Middle Eastern', 'Middle Eastern'),
        ('South Asian', 'South Asian'),
        ('Others', 'Others'),
        ('Black', 'Black'),
        ('Hispanic', 'Hispanic'),
        ('Latino', 'Latino'),
    ], validators=[InputRequired()])
    Family_mem_with_ASD = SelectField('Family member with ASD', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    A10_score = IntegerField('A10-score', validators=[NumberRange(min=1, max=10), InputRequired()])
