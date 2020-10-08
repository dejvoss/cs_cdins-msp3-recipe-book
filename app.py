# Recipe Book Application
# Flask application for website recipe book
# Application display recipes from database mongoDB and allowed user to add recipes to the database

import os
from flask import Flask, render_template, redirect, request, url_for, flash, make_response
import email_validator
import pdfkit
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import forms
from forms import InsertRecipeForm, ContactForm, SendRecipeForm, meal_type_list, measureList, category_list
from bson.objectid import ObjectId
from bson.json_util import dumps

# import variables setted in environment file if exist
if os.path.exists("env.py"):
    import env



# set upload folder and allowed extension for uploading recipe image
UPLOAD_FOLDER = 'static/uploaded_img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# congifguration variables
app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_book'              # database collection name
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')   
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# configuration for email server used to send contact message and/or sending recipe to email
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= '465'
app.config['MAIL_USE_SSL']= True
app.config['MAIL_USERNAME']= os.environ.get('MAIL_USERNAME')
app.config['MAIL_DEFAULT_SENDER']= os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD']= os.environ.get('MAIL_PASSWORD')

mail = Mail(app)
mongo = PyMongo(app)
db = mongo.db.recipes

# home route, display all recipes
@app.route('/')
@app.route('/home')
def home():
    contactForm = ContactForm()
    categories = meal_type_list #variable to retrive category buttons in home page
    return render_template("index.html", recipes=mongo.db.recipe_base.find(), contactForm=contactForm, categories=categories, len=len(categories))

# Route to display only recipe in selected category and show flash message if selected category doesn't exist
@app.route('/home/<category_name>')
def displayCategory(category_name):
    if category_name in category_list :
        contactForm = ContactForm()
        return render_template('index.html', recipes=mongo.db.recipe_base.find( { 'meal_type': category_name } ), contactForm=contactForm, categories=meal_type_list, len=len(meal_type_list))
    else:
        flash('Category doesn\'t exist Pick a proper one', 'warning')
        return redirect(url_for('home'))

# route display form for inserting new recipe
@app.route('/add_recipe')
def add_recipe():
    contactForm = ContactForm()
    form = InsertRecipeForm()
    return render_template("add_recipe.html", form=form, contactForm=contactForm)

# function to check if uploaded file has correct extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route which populate new recipe from form in to mongoDB database
@app.route('/insert_recipe', methods=['GET','POST'])
def insert_recipe():
    form = InsertRecipeForm()

    if form.validate_on_submit():
        mongo_recipe_object = request.form.to_dict() # create recipe object, by changing request form in to dictionary
        ingredients_name_only = {k:v for k,v in mongo_recipe_object.items() if "ingredient" in k and "name" in k} # filtered recipe object - take only ingredients name to push to ingredient database and to count how many ingredients is in recipe
        nr_of_ingredients = int(len(ingredients_name_only)) #count how many ingrdients is in recipe
        mongo_recipe_object['amount_of_ingred'] = nr_of_ingredients # add number of ingredients to database to recipe object
        # check each of ingredient if exist in ingredient base and add if not exist 
        # - it is for feature to give for user opportunity to pick up ingredients instead of typing manually
        for k, v in ingredients_name_only.items():  
            if mongo.db.ingredients_list.find({'name': v}).count() == 0:
                mongo.db.ingredients_list.insert_one({'name': v})
        # check if uploaded image exist and if is correct, if yes, then save file to upload folder
        # if not then display flash message
        # save name of file to recipe object
        # and in end add new recipe to database
        if 'meal_image' not in request.files: 
            flash('It looks like you did not select any file', 'warning')
            flash('You can press back in your browser to restore recipe data you filled in', 'info')
            return redirect(url_for('add_recipe'))
        file = request.files['meal_image']

        if file.filename =='':
            flash('It looks like you did not select any file', 'warning')
            flash('You can press back in your browser to restore recipe data you filled in', 'info')
            return redirect(url_for('add_recipe'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            meal_name = request.form['recipe_name']
            saved_filename = meal_name + '_' + filename # create a filename base on the file name and recipe name
            saved_filename = secure_filename(saved_filename)
            path=os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(path)
            mongo_recipe_object["meal_image"]=saved_filename
            mongo.db.recipe_base.insert_one(mongo_recipe_object)
            flash('I have one more delicious recipe now. Thank you!', 'success')
            return redirect(url_for('home'))

        else:
            flash('It looks like you select not correct image file', 'warning')
            flash('You can press back in your browser to restore recipe data you filled in', 'info')
            return redirect(url_for('add_recipe'))

    flash('Something went wrong. Please try again.', 'warning') #flash message in case the form doesn't go thru validation
    flash('You can try press back in your browser to restore recipe data you filled in', 'info')
    return redirect(url_for('add_recipe'))

# route display recipe in single page
@app.route('/recipes/<recipe_id>')
def single_recipe(recipe_id):
    contactForm = ContactForm()
    recipe = mongo.db.recipe_base.find_one({'_id': ObjectId(recipe_id)})
    ingredients = {k:v for k,v in recipe.items() if "ingredient" in k}
    mailRecipe = SendRecipeForm()
    return render_template('singl_recipe.html', recipe=recipe, ingredients=ingredients, contactForm=contactForm, mailRecipe=mailRecipe)

# remove recipe from database
@app.route('/delete/<recipe_id>')
def delete_recipe(recipe_id):
    recipe = mongo.db.recipe_base.find_one({'_id': ObjectId(recipe_id)})
    recipe_name = recipe['recipe_name']
    # if recipe has image assigned then remove image and record in database, if not, then remove only the record in database
    if 'meal_image' in recipe:
        recipe_img = recipe['meal_image']
        path=os.path.join(app.config['UPLOAD_FOLDER'], recipe_img)
        os.remove(path)
        mongo.db.recipe_base.remove({'_id': ObjectId(recipe_id)})
        flash('Recipe ' + recipe_name + ' removed from database successfully.', 'success')
        return redirect(url_for('home'))
    else:
        mongo.db.recipe_base.remove({'_id': ObjectId(recipe_id)})
        flash('Recipe ' + recipe_name + ' removed from database successfully.', 'success')
        return redirect(url_for('home'))

# page route for editing recipe - display InsertRecipeForm with populated data from database
@app.route('/edit-recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe = mongo.db.recipe_base.find_one({'_id': ObjectId(recipe_id)})
    contactForm = ContactForm()
    form = InsertRecipeForm()
    return render_template('edit_recipe.html', form=form, contactForm=contactForm, recipe=recipe)

# update recipe in database - used replace_one instead of update_one as this way is much easier in case of removing ingredients or preparation steps
@app.route('/update/<recipe_id>', methods=['GET','POST'])
def update_recipe(recipe_id):
    recipe_base = mongo.db.recipe_base  
    new_recipe = request.form.to_dict()
    form = InsertRecipeForm()
    # validate form
    if form.validate_on_submit():
        old_recipe = recipe_base.find_one({'_id': ObjectId(recipe_id)})                    
        ingredients_name_only = {k:v for k,v in new_recipe.items() if "ingredient" in k and "name" in k} # filtered recipe object - take only ingredients name to count number of ingrdients
        nr_of_ingredients = int(len(ingredients_name_only)) #count how many ingrdients is in recipe
        new_recipe['amount_of_ingred'] = nr_of_ingredients # add number of ingredients to database to recipe object
        old_recipe = recipe_base.find_one({'_id': ObjectId(recipe_id)}) 
        old_filename = old_recipe['meal_image'] 
        if 'meal_image' not in request.files:   # if there is no new file, save old file in new recipe object                           
            new_recipe["meal_image"] = old_filename  
        file = request.files['meal_image']
        # if selected  file has wrong extension display flash message
        if file and not allowed_file(file.filename):
            flash('It looks like you want to update meal image, but you didn\'t select correct file', 'warning')
            return redirect(url_for('edit_recipe', recipe_id=recipe_id))
        if file.filename == '':              # if new file is not selected, save old file in new recipe object                           
            new_recipe["meal_image"] = old_filename  
        # if new file is selected, update database accordingly
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            meal_name = request.form['recipe_name']
            saved_filename = meal_name + '_' + filename # create a filename base on the file name and recipe name
            saved_filename = secure_filename(saved_filename)
            path=os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(path)
            new_recipe["meal_image"] = saved_filename  
            path=os.path.join(app.config['UPLOAD_FOLDER'], old_filename)     # remove old file as new was saved
            os.remove(path)
        # save old file in other cases
        else:                         
            new_recipe["meal_image"] = old_filename
        # update database by replacing old recipe object
        recipe_base.replace_one({'_id': ObjectId(recipe_id)}, new_recipe)   # replace recipe object by new one
        flash('Recipe updated. Thank you!', 'success')
        return redirect(url_for('single_recipe', recipe_id=recipe_id))  
    flash('Something went wrong. Please try again.', 'warning')
    return redirect(url_for('edit_recipe', recipe_id=recipe_id))
        

# route for sending contact message
@app.route('/contact', methods=['GET','POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # data from form
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        # send message
        mailMsg = Message(subject=subject, sender=email, recipients=['deosiecki@gmail.com'])
        mailMsg.body = 'You receive messaege: ' + message + 'from ' + name + 'who use email address ' + email
        mailMsg = Message(subject=subject, sender=email, recipients=['deosiecki@gmail.com'])
        mail.send(mailMsg)
    flash("Something went wrong, message doesn't send. Please try again", 'warning')
    return redirect(url_for('home'))

# route for sending recipe by email
@app.route('/send-recipe-to-email/<recipe_id>', methods=['GET', 'POST'])
def send_mail_recipe(recipe_id):
    form = SendRecipeForm()
    # check if form is validate - there are only email to validate, take the data
    if form.validate_on_submit():
        recipe = mongo.db.recipe_base.find_one({'_id': ObjectId(recipe_id)}) # find recipe in database
        ingredients = {k:v for k,v in recipe.items() if "ingredient" in k}
        subject = "Your recipe for"
        emailto = request.form['emailto']
        recipeMsg = Message(subject=subject, recipients=[emailto])
        recipeMsg.html = render_template('mail_recipe.html', recipe=recipe, ingredients=ingredients) # populate recipe to the html template and send as email
        mail.send(recipeMsg)
        flash('Recipe succesfully send on your email address.', 'success')
        return redirect(url_for('single_recipe', recipe_id=recipe_id))
    flash('Somethin went wrong, check your email address and try again.', 'warning')
    return redirect(url_for('single_recipe', recipe_id=recipe_id))

#show flash message for user in case of errors and return to home page
# @app.errorhandler(Exception)
# def handle_bad_request(e):
#     """ Error handling: will catch these errors and display the play messages to error.html """
#     if type(AttributeError):
#         flash('Recipe doesn\'t exist. You can add one.', 'info')
#         print(type(e))
#         return redirect(url_for('home'))
#     flash('This action occur error. Please try different one', 'info')
#     print(type(e))
#     return url_for("home")



# route for downloading pdf version of recipe by using wkhtmltopdf which work fine on local machine - works fine, but with few conditions:
# wkhtmltopdf needs to be installed and added to the windows path (please refer to https://www.youtube.com/watch?v=Y2q_b4ugPWk)
# unfortunetally i couldn't run it on heroku.
# I find many ways to fix in stackoverflow, but any of these works for me or i was not able implement these as should be
# in case that i have also print function which is giving similar output as the pdf and instead of print every user can save file to pdf i decide to comment the wkhtmltopdf function
# and leave only the print one
# Please uncomment function on local server if needed
# @app.route('/pdf/<recipe_name>')
# def pdf_template(recipe_name):
#     recipe=mongo.db.recipe_base.find_one({'recipe_name': recipe_name})
#     ingredients = {k:v for k,v in recipe.items() if "ingredient" in k}
#     rendered = render_template('pdf_template.html', recipe=recipe, ingredients = ingredients)
#     css = ['static/css/pdf-css.css']
#     pdf = pdfkit.from_string(rendered, False, css=css)
#     response = make_response(pdf)
#     disposCont = 'inline; filename=' + recipe_name + '.pdf'
#     response.headers['Content-Type'] = 'appplication/pdf'
#     response.headers['Content-Disposition'] = disposCont
#     return response

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

