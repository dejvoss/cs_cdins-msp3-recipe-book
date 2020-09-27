# Recipe App
# Flask application for website recipe book
import os
from flask import Flask, render_template, redirect, request, url_for, flash, make_response
import email_validator
import pdfkit
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, TextAreaField, FileField, SelectField, IntegerField, FormField, Form, FieldList
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional, Email


if os.path.exists("env.py"):
    import env
    
if 'DYNO' in os.environ:
    print ('loading wkhtmltopdf path on heroku')
    WKHTMLTOPDF_CMD = subprocess.Popen(
        ['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf-pack')], # Note we default to 'wkhtmltopdf' as the binary name
        stdout=subprocess.PIPE).communicate()[0].strip()
else:
    print ('loading wkhtmltopdf path on localhost')
    MYDIR = os.path.dirname(__file__)    
    WKHTMLTOPDF_CMD = os.path.join(MYDIR + "/static/executables/bin/", "wkhtmltopdf.exe")

UPLOAD_FOLDER = 'static/uploaded_img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_book'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER']= os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT']= os.environ.get('MAIL_PORT')
app.config['MAIL_USE_SSL']= os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USE_TLS']= os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME']= os.environ.get('MAIL_USERNAME')
app.config['MAIL_DEFAULT_SENDER']= os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD']= os.environ.get('MAIL_PASSWORD')

mail = Mail(app)
mongo = PyMongo(app)
db = mongo.db.recipes

measureList=[('grams', 'grams'), ('decagrams', 'decagrams'), ('pieces', 'pieces'), ('pinch', 'pinch'), ('glasses', 'glasses'), ('liters', 'liters'), ('spoons', 'spoons'), ('tea spoons', 'tea spoons')]
meal_type_list=[('warm_meals', 'Warm meals'), ('cold_meals', 'Cold meals'), ('drinks', 'Drinks'), ('desserts', 'Desserts')]
# msg=Message("Subject", recipients=['recipient1@example.com'])
# msg.body ="Mail Body"

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
    submit = SubmitField('Send')
    
@app.route('/')
@app.route('/home/get_recipes')
def home():
    contactForm = ContactForm()
    categories = meal_type_list
    return render_template("index.html", recipes=mongo.db.recipe_base.find(), contactForm=contactForm, categories=categories, len=len(categories))

@app.route('/home/warm_meals')
def warm_meals():
    contactForm = ContactForm()
    categories = meal_type_list
    return render_template("index.html", recipes=mongo.db.recipe_base.find( { 'meal_type': 'warm_meals' } ), contactForm=contactForm, categories=categories, len=len(categories))

@app.route('/home/cold_meals')
def cold_meals():
    contactForm = ContactForm()
    categories = meal_type_list
    return render_template("index.html", recipes=mongo.db.recipe_base.find( { 'meal_type': 'cold_meals' } ), contactForm=contactForm, categories=categories, len=len(categories))

@app.route('/home/drinks')
def drinks():
    contactForm = ContactForm()
    categories = meal_type_list
    return render_template("index.html", recipes=mongo.db.recipe_base.find( { 'meal_type': 'drinks' } ), contactForm=contactForm, categories=categories, len=len(categories))

@app.route('/home/desserts')
def desserts():
    contactForm = ContactForm()
    categories = meal_type_list
    return render_template("index.html", recipes=mongo.db.recipe_base.find( { 'meal_type': 'desserts' } ), contactForm=contactForm, categories=categories, len=len(categories))

@app.route('/add_recipe')
def add_recipe():
    contactForm = ContactForm()
    form = InsertRecipeForm()
    list_of_ingred = mongo.db.ingredients_list.find()
    return render_template("add_recipe.html", form=form, list_of_ingredients=list_of_ingred, contactForm=contactForm)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/insert_recipe', methods=['GET','POST'])
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
            saved_filename = meal_name + '_' + filename
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

@app.route('/recipes/<recipe_name>')
def single_recipe(recipe_name):
    contactForm = ContactForm()
    recipe=mongo.db.recipe_base.find_one({'recipe_name': recipe_name})
    ingredients = {k:v for k,v in recipe.items() if "ingredient" in k}
    return render_template('singl_recipe.html', recipe=recipe, ingredients=ingredients, contactForm=contactForm)

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        meilMsg=Message(subject=subject, sender=email, recipients=['deosiecki@gmail.com'])
        meilMsg.body = message + name
        mail.send(meilMsg)
        return "Email send succesful"

@app.route('/pdf/<recipe_name>')
def pdf_template(recipe_name):
    recipe=mongo.db.recipe_base.find_one({'recipe_name': recipe_name})
    ingredients = {k:v for k,v in recipe.items() if "ingredient" in k}
    rendered = render_template('pdf_template.html', recipe=recipe, ingredients = ingredients)
    css = ['static/css/pdf-css.css']
    pdf = pdfkit.from_string(rendered, False, css=css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'appplication/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=your-file-name.pdf'
    return response
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

