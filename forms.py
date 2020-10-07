# form classes for recipe book app
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, TextAreaField, FileField, SelectField, IntegerField, FormField, Form, FieldList
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional, Email

# list of measures used in add recipe form
measureList=[('grams', 'grams'), ('decagrams', 'decagrams'), ('pieces', 'pieces'), ('pinch', 'pinch'), ('glasses', 'glasses'), ('liters', 'liters'), ('spoons', 'spoons'), ('tea spoons', 'tea spoons')]
#  list of recipes categories, add it here in case of new category, 
#  meal_type_list is used to insertRecipe form for option tag in select input, 
#  categoryList is used for displayin recipes by category in home page
meal_type_list=[('Warm meals', 'Warm meals'), ('Cold meals', 'Cold meals'), ('Drinks', 'Drinks'), ('Desserts', 'Desserts')]
category_list = ['Warm meals', 'Cold meals', 'Drinks', 'Desserts']
# ingredients form for Insert recipe form
class Ingredients(Form):
    name = StringField('Ingredient name', validators=[InputRequired()])
    amount = DecimalField('Amount', validators=[InputRequired()])
    measure = SelectField('Measure', choices=measureList, validators=[InputRequired()])
# preparation form for Insert recipe form
class Preparations(Form):
    step = TextAreaField('Preparation step', validators=[InputRequired()])
# insert recipe form for inserting new recipe to database
class InsertRecipeForm(FlaskForm):
    recipe_name = StringField('Recipe name', validators=[InputRequired()])
    meal_type = SelectField('Meal type', choices=meal_type_list, validators=[DataRequired()])
    preparation_time = IntegerField('Preparation time (minutes)', validators=[DataRequired(), NumberRange(min=5, max=180)])
    portions = IntegerField('Amount of portions', validators=[DataRequired(), NumberRange(min=1, max=6)])
    meal_description = TextAreaField('Meal description', validators=[Optional()])
    ingredients = FieldList(FormField(Ingredients), min_entries=3)
    preparation = FieldList(FormField(Preparations), min_entries=1)
    meal_image = FileField('Meal picture')
# contact form - used to send contact email
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')
# form used to sending the email with meal recipe to user
class SendRecipeForm(FlaskForm):
    emailto = StringField('email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Send recipe')