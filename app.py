# Recipe App
# Flask application for website recipe book
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import datetime

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.JPG', '.PNG', '.GIF']


mongo = PyMongo(app)

@app.route('/')
@app.route('/home/get_recipes')
def home():
    return render_template("index.html", recipes=mongo.db.recipes.find())

@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html")

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
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
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

