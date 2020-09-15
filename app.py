# Recipe App
# Flask application for website recipe book
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, TextAreaField, FileField, SelectField, IntegerField, FormField, Form, FieldList
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional


if os.path.exists("env.py"):
    import env

UPLOAD_FOLDER = 'media/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.jinja_env.filters['b64d'] = lambda u: b64encode(u).decode()
app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



mongo = PyMongo(app)
db = mongo.db.recipes

measureList=[('g', 'grams'), ('dec', 'decagrams')]
meal_type_list=[('warm_meal', 'Warm meal'), ('cold_meal', 'Cold meal'), ('drink', 'Drink')]

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
    ingredients = FieldList(FormField(Ingredients), min_entries=5)
    preparation = FieldList(FormField(Preparations), min_entries=3)
    meal_image = FileField('Meal picture')
    

@app.route('/')
@app.route('/home/get_recipes')
def home():

    return render_template("index.html", recipes = mongo.db.recipes.find())
# def ImgURL(url):
#     img = urllib.urlopen(url).read()
#     encoded_string = base64.b64encode(img)
#     return encoded_string


@app.route('/add_recipe')
def add_recipe():
    form = InsertRecipeForm()
    return render_template("add_recipe.html", form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    if request.method == 'POST':
        mongo_recipe_object = request.form.to_dict()
        if 'meal_image' not in request.files:
            return "No file"
        file = request.files['meal_image']
        if file.filename =='':
            return "Empty file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            meal_name = request.form['recipe_name']
            saved_filename = meal_name + '_' + filename
            path=os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(path)
            mongo_recipe_object["meal_image"]=path
            print(mongo_recipe_object)
            return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

