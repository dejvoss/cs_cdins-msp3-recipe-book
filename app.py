# Recipe App
# Flask application for website recipe book
import os
from flask import Flask, render_template, redirect, request, url_for
import email_validator
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, TextAreaField, FileField, SelectField, IntegerField, FormField, Form, FieldList
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional, Email


if os.path.exists("env.py"):
    import env

UPLOAD_FOLDER = 'static/uploaded_img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



mongo = PyMongo(app)
db = mongo.db.recipes

measureList=[('grams', 'grams'), ('decagrams', 'decagrams'), ('pieces', 'pieces'), ('pinch', 'pinch'), ('glasses', 'glasses'), ('liters', 'liters'), ('spoons', 'spoons'), ('tea spoons', 'tea spoons')]
meal_type_list=[('warm meal', 'Warm meal'), ('cold meal', 'Cold meal'), ('drink', 'Drink')]

class Ingredients(Form):
    name = StringField('Ingredient name', validators=[InputRequired()])
    amount = DecimalField('Amount', validators=[InputRequired()])
    measure = SelectField('Measure', choices=measureList, validators=[InputRequired()])

class Preparations(Form):
    step = TextAreaField('Preparation step', validators=[InputRequired()])

class InsertRecipeForm(FlaskForm):
    recipe_name = StringField('Recipe name', validators=[InputRequired()])
    meal_type = SelectField('Meal type', choices=meal_type_list, validators=[DataRequired()])
    preparation_time = IntegerField('Preparation time (minutes)', validators=[DataRequired(), NumberRange(min=5, max=180)])
    portions = IntegerField('Amount of portions', validators=[DataRequired(), NumberRange(min=1, max=6)])
    meal_description = TextAreaField('Meal description', validators=[Optional()])
    ingredients = FieldList(FormField(Ingredients), min_entries=3)
    preparation = FieldList(FormField(Preparations), min_entries=1)
    meal_image = FileField('Meal picture')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    
@app.route('/')
@app.route('/home/get_recipes')
def home():
    contactForm = ContactForm()
    return render_template("index.html", recipes=mongo.db.recipe_base.find(), contactForm=contactForm)

@app.route('/home/warm_meals')
def warm_meals():
    contactForm = ContactForm()
    return render_template("index.html", recipes=mongo.db.recipe_base.find( { 'meal_type': 'warm meal' } ), contactForm=contactForm)

@app.route('/add_recipe')
def add_recipe():
    contactForm = ContactForm()
    form = InsertRecipeForm()
    list_of_ingred = mongo.db.ingredients_list.find()
    return render_template("add_recipe.html", form=form, list_of_ingredients=list_of_ingred, contactForm=contactForm)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    if request.method == 'POST':
        mongo_recipe_object = request.form.to_dict()
        ingredients_name_only = {k:v for k,v in mongo_recipe_object.items() if "ingredient" in k and "name" in k}
        nr_of_ingredients = int(len(ingredients_name_only))
        mongo_recipe_object['amount_of_ingred'] = nr_of_ingredients
        for k, v in ingredients_name_only.items():
            if mongo.db.ingredients_list.find({'name': v}).count() == 0:
                mongo.db.ingredients_list.insert_one({'name': v})
        if 'meal_image' not in request.files:
            return "No file"
        file = request.files['meal_image']
        if file.filename =='':
            return "Empty file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            meal_name = request.form['recipe_name']
            saved_filename = meal_name + '_' + filename
            saved_filename = secure_filename(saved_filename)
            path=os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(path)
            mongo_recipe_object["meal_image"]=saved_filename
            mongo.db.recipe_base.insert_one(mongo_recipe_object)
            return redirect(url_for('home'))

@app.route('/recipes/<recipe_name>')
def single_recipe(recipe_name):
    contactForm = ContactForm()
    recipe=mongo.db.recipe_base.find_one({'recipe_name': recipe_name})
    ingredients = {k:v for k,v in recipe.items() if "ingredient" in k}
    return render_template('singl_recipe.html', recipe=recipe, ingredients=ingredients, contactForm=contactForm)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

