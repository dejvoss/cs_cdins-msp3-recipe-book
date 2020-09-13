# Recipe App
# Flask application for website recipe book
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import datetime
import base64
from base64 import b64encode
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SubmitField, TextAreaField, FileField, SelectField, IntegerField, FormField, Form, FloatField, FieldList
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional


if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.jinja_env.filters['b64d'] = lambda u: b64encode(u).decode()
app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF']
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


mongo = PyMongo(app)
db = mongo.db.recipes

measureList=[('g', 'grams'), ('dec', 'decagrams')]

class Ingredients(Form):
    name = StringField('Ingredient name')
    amount = DecimalField('Amount')
    measure = SelectField('Measure', choices=measureList)

class Preparations(Form):
    step = TextAreaField('Preparation step')

class InsertRecipeForm(FlaskForm):
    recipe_name = StringField('Recipe name', validators=[InputRequired()])
    meal_type = SelectField('Meal type', choices=[('warm_meal', 'Warm meal'), ('cold_meal', 'Cold meal'), ('drink', 'Drink')], validators=[DataRequired()])
    preparation_time = IntegerField('Preparation time (minutes)', validators=[DataRequired(), NumberRange(min=5, max=180)])
    portions = IntegerField('Amount of portions', validators=[DataRequired(), NumberRange(min=1, max=6)])
    meal_description = TextAreaField('Meal description', validators=[Optional()])
    ingredients = FieldList(FormField(Ingredients), min_entries=5)
    preparation = FieldList(FormField(Preparations), min_entries=3)

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

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    # create uniq name for meal image and store as decoded object in mongodb
    todaysDate = datetime.datetime.now()    #today date and time for imange file name
    string_date = todaysDate.strftime("%Y%m%d %H:%M:%S") # convert date, time to string
    recipe = mongo.db.recipes # database collection
    recipe_object = request.form.to_dict() # render the html for to the dictionary object
    meal_img = request.files['meal_image'] # uploaded image of meal
    meal_img = secure_filename(meal_img.filename) # change name of image by secure_filename
    my_img_name = recipe_object["recipe_title"] + '.' + string_date + '.' + meal_img #create own file name to be uniq
    mongo.save_file(my_img_name, request.files["meal_image"]) # save img meal file to the mongo database
    recipe_object['meal_image'] = my_img_name #change the name of recipe image to own name created above(my_img_name)
    recipe.insert_one(recipe_object) #insert recipe_object to the database
    # insert ingredients to the ingredient database collection
    ingredient_base = mongo.db.ingredients_list
    filtered_recipe_object = {k:v for k,v in recipe_object.items() if "ingredient" in k}
    for k,v in filtered_recipe_object.items():
        if ingredient_base.find( {"name": v} ).count() == 0:
            if v != "":
                ingredient_base.insert_one({"name": v})
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

