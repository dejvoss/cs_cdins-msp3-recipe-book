# cdins-msp3-recipe-book - Code Institute Milestone Project 3 - Recipe Book

Recipe book is a project of website with meals recipes. Project is a practicing the skills of python, flask and mongoDB during my study of Full Stack Web Development in Code Institiute. 

## UX

### Strategy

The main goal of this project is to give for the users nice looked website with meals recipes. Other goal is to give possibility for users to add the meals recipes which will be displayed on a webpage. I have done research and below user stories describe the user needs for my webpage. 

#### User Stories:

I identified 2 group of user for my project. People between the age of 25 and 45 and people over the age of 45. My user stories are pieces of conversation about a website.

#### People between the age of 25 and 45:

1. Propably i could use that kind of site to find idea for dinner, so i would like to see straight away delicious meals on the first page. Inserting recipes must be easy.
2. When i will find a recipe i would like to print the shopping list.
3. I would like to find recipes based on the ingredients which i have at home.
4. I wish to select the meals depence of the quantity of ingredients and the preparation time.
5. The recipe needs to have picture, ingredients list and preparation steps.

#### People over the age of 45:

1. I would like to have place in the internet when i can find meal recipes as a plain text, not video, i cannot cook and watch. I prefer to read the recipe first and then cook. The first view of page? - I want to see there good ideas for a dinner. Ingredients must be shown definitevly in piece, spoons and glasses, weight is good for people who is on a diet. I like to eat well.
2.  I still have my notebook with recipes - i like to look in to the piece of paper during cooking. Printing the recipe from web it could be a good feature. I could share my notebook, if inserting recipes will be easy i could put my recipes to internet by myself.
3. Pictures are not really necessary if the title and description is good.

### Scope

Taking to consideration the above user stories i identified below requirements:

#### Functional Requirements:
1. The project must be a multi webpage with main page, page for adding recipes and single recipe page.
2. Each recipes needs to be able to open as a single webpage.
3. Website must be accesible from different devices.
4. Inserting new recipe must be easy and intuitive:
    * selecting category from list
    * selecting preparation time from list
    * selecting portions quantity from list
    * typing meal name
    * description, but not required
    * typing ingredients
    * type ingredients quantity
    * select measure (grams, pieces, spoons, )
    * 5 fields in default and plus button for more ingredients fields (during creating page i decide to display only 3 fields in default and create plus/minus buttons to add or remove fields)
    * preparation typed in steps with 3 default and button for adding next step (during creating page i decide to display only 1 fields in default and create plus/minus buttons to add or remove fields)
    * button for uploading image
    * save button
5. User has to have possibility to download/print ingredients list.
6. User needs to have possibility to browse recipes by different categories.
7. Navigation bar needs to display categories.

#### Design Requirements:

1. Main page should display big photo or video of cooking meal as background. 
2. On the front of page needs to be big button with find recipe text which is going to move user to middle of webiste - where the recipes will be.
3. In middle of website should be displayed recipes in 2 or 3 columns in big screens and 1 column on the small screens.
4. Recipes needs to be displayed with photo, title and icons for preparation time and portions quantity.
5. By clicking on meal image is turning in to the ingredients list and preparation steps with button to open recipe in new window.
6. Menu needs to be small but visible.

#### Content Requirements:

1. Recipe should described:
    * category
    * preparation time
    * portions quantity
    * meal name
    * description
    * ingredients
    * ingredients quantity
    * ingredient measure (grams, pieces, spoons, )
    * image
2. Rrecipes needs to be displayed on main page.
3. Meals has to be organized by different categories:
    * cold meals
    * hot meals
    * drinks
    * desserts

### Structure

![Web Page Structure](README_purpose/web_structure.PNG)

Scheme of database structure were changed a bit - due to low number of categories i resign from keeping these in database. 
Instead i create collection with ingredients to give in future possibility for autocomplete ingredients fields during adding recipe to raise user experience.
### Skeleton

#### Desktop
![Web Page Structure](README_purpose/main_page_wfr.PNG)
![Web Page Structure](README_purpose/recipe_page_wfr.PNG)
![Web Page Structure](README_purpose/insert_recipe_wfr.PNG)

#### Mobile
![Web Page Structure](README_purpose/mb_main_page_wfr.PNG)
![Web Page Structure](README_purpose/mb_recipe_page_wfr.PNG)
![Web Page Structure](README_purpose/mb_insert_recipe_wfr.PNG)

### Surface

#### Main picture

As a end of the designing my webpage i decide to choose the main image/movie which will be displayed on the main page and then matching colors scheme. 
I wanted to put a picture that arouses appetite and ecourages cooking. This is what I found.

![Web Page Structure](README_purpose/main_image.png)

#### Colours

Based on the main pictures and using the Huesnap tool[Huesnap.com] I selected below color scheme for my website.

1. #5e8b4a
2. #ca2545
3. #a57255 - not used in the end
4. #0a0904

![Web Page Structure](README_purpose/color_scheme.png)

#### Fonts

I choose two combinaion of fonts which i like before creating a webpage. I take to consideration that it could look different in the end effect than i imagined. 


<link href="https://fonts.googleapis.com/css?family=Archivo+Black|Judson:400,700" rel="stylesheet">
body {
 font-family: 'Judson', serif;
}

h1, h2, h3, h4, h5, h6 {
 font-family: 'Archivo Black', sans-serif;
}

<link href="https://fonts.googleapis.com/css?family=Abril+Fatface|Roboto:300,700" rel="stylesheet">
body {
 font-family: 'Roboto', sans-serif;
 font-weight: 300;
}

h1, h2, h3, h4, h5, h6 {
 font-family: 'Abril Fatface', serif;
}

In the end i select combination of above fonts and remove font-weight settings:

body {
 font-family: 'Roboto', sans-serif;
 
}

h1, h2, h3, h4, h5, h6 {
 font-family: 'Archivo Black', sans-serif;
}

## Features

1. Insert recipe to the database - allows users to add own recipes.
2. Add recipe image - allows users to add meal image to the recipes
3. Printing recipe - allows users to print recipe without navigation bar and footer - only clean reicpe page.
4. Sending recipe by email - allows users to send recipe to email.
5. Contact form - allows users to leave contact message.
6. Navigation bar - allows users to easily navigate the site.
7. Display recipes by categories - Big navigation bar above the recipes allows users to select categories to display recipes only from selected category.
8. Icons displayed below each recipe with portion quantity, preparation time, type of meal and number of ingredients - Allows users to find quickly what kind of meal it is, how long it takes to prepare, for how many people it is and how many ingredients is used to prepare.
9. Inserting ingredients name to ingredients base during inserting new recipe.

## Features left to implement
1. Download recipe as PDF.
2. Option to select recipes by number of ingredients.
3. Create autocomplete function for typing ingredients with database ingredient collection as source.

## Technologies Used

* python - provides background logic on website
* flask - allowed to display python logic in web browser
* MongoDB - python extension for manipulation mongoDB database
* Flask-WTF - flask forms used to display and take data from contact and add recipe forms.
* Flask-Mail - used to send email messages
* Bootstrap 5 Alpha - used to create layout of the pages, navigation bar and footer.
* CSS - provide website style
* HTML - provides content of the website
* JAVASCRIPT - provides function for interaction users with website
* BOOTSTRAP ICONS - used to enhance the user experience
* GOOGLE FONT - provides main fonts for website
* MONGODB - Database for storing recipes
* HERKOU - deployment service
* Git for version control
* github - for keeping remote repository
* VSCode - code editor used during wiriting this application

For more and all python extensions used in this app, please read the requirements.txt file.

## Testing

I did test features after implementation and after each change in code. I also perform complete test in end of the project. The below review is not in the order that I ran the tests because these are all the tests that got my attention.

### Testing responsiveness and design

I did test my website all the time during creating in browser developer to see if the page is responsive at mobile screens and at large screens. I used 3 different web browser during tests and creating page:
* Google Chrome Version 85.0.4183.121 (Official Build) (64-bits)
* Brave Version 1.14.84 Chromium: 85.0.4183.121 (Official Build) (64-bit)
* Microsoft Edge 85.0.564.68 (Official Build) (wersja 64-bit)
* Firefox 72.0.2 (64-bit

I did also test the page on different screens and systems as below:
* Android v10
* Windows with screen of 15'
* Windows with screen of 17'
* Windows with screen 24'

I constently share the page with my friends and family to test design.

### Testing JavaScript functions

1. scrollFunction
    * Check if menu is changing collor when scroll window down. Perform chck on different type of page - add recipe, home, single recipe, edit recipe.
        * Test passed.
2. myFunction - function to stop/play video
    * Click on control button to stop video, click to play. Check if video reacting as should be(stop and play) and check if button is changin icon. Wait till video will be finished, check if button change icon.
        * Test passed.
3. addIngredientField
    * Click on plus button in add recipe page to see if new ingredient field is added.
        * Test passed.
    * Fill in ingredients field and click on plus button to see if new field is added.
        * Test failed - new field were added, but all filled in fields are cleared.
        * Fix: replace innerHtml by appenChild.
    * Repeat second test.
        * Test passed.
4. removeIngredientField
    * Click on minus button to see if ingredient field is removed.
        * Test passed in 90% - new fields are removed automatically, but for 3 fields which are on the page from beggining, need to click double time to remove it.
5. addStepField
    * Click on plus button in add recipe page to see if new step field is added.
        * Test passed.
    * Fill in preparation steps field and click on plus button to see if new field is added.
        * Test failed - new field were added, but all text from other fields is cleared.
        * Fix: replace innerHtml by insertAdjacentHTML. I decide to use different way than in point 3 to practice skills.
    * Repeat second test.
        * Test passed.
6. removeStepField
    * Click on minus button to see if ingredient field is removed.
        * Test passed in 90% - new fields are removed automatically, but for 3 fields which are on the page from beggining, need to click double time to remove it.
7. PreviewImage
    * Upload image and check if appear in preview box.
        * Test passed.
8. openNav
    * Click on mobile navigation button to see if mobile menu is openning.
        * Test passed.
9. closeNav
    * Click on X button in navigation menu to see if menu is closed.
        * Test passed
10. printRecipe
    * Click on printRecipeButton to see if print window is open.
        * Test failed - Print window is open, but in printPreview are navigation bar and footer - i don't want force user to print all this, when he want to print recipe.
            * Fix - adjust function to open new window and place to it only the part with recipe. Then open print preview.
        * Repeat test.
            * Test passed.
11. showConfirmMsg
    * Click on remove rcipe button in single recipe page to see if message with warning and buttons will popup.
        * Test passed.
12. closeConfirmMsg 
    * Click on 'Cancel delete recip' button which has in text 'I will think about it' to see if popup warning message will dissappear.
        * Test passed.

### Test python functionality

1. home route
    1. Check if link to home page is work from all other pages:
        -   click on home link in footer in different type of page: add recipe, home, single recipe, edit recipe, to see if web browser is directing to home page,
        -   click on logo link in navigation bar in different type of page: add recipe, home, single recipe, edit recipe, to see if web browser is directing to home page,
        -   click on home link in mobile menu in different type of page: add recipe, home, single recipe, edit recipe, to see if web browser is directing to home page
        * Test passed for all 3 links.
    2. Check if all recipes are populated from database and displayed in home page.
        * Test passed.
    3. Check if all data about recipes are displayed.
        * Test passed.
    4. Check if all recipe data are displayed correctly.
        * Test failed:
            -   icons which descripe type of meal are not displayed.
            -   Fix: category names in database are different than in function for displaying meal icons; change the values for the same ones.
        * 2nd test passed.
2. displayCategory route
    1. Click on each category name to see if different (corrected) meals are displayed.
        * Test failed:
            -   select option in add recipe page has value different than displayed text. Category links are build base on displayed text, recipes in database has values of select options.
            -   Fix: change the names of values and displayed values to the same ones. Populate the category buttons from the same list which is used to the add recipe form in case of new category it could be added in one place instead of many. Apply fix also to mobile links.
        * 2nd test passed.
    2. Click on each category name in mobile view to see if different (corrected) meals are displayed.
        * Test passed.
3. add_recipe
    1. Click on 4 different links(mobile menu, navigation bar, button in home page, footer menu) Add recipe in navigation bar to see if add recipe page is open.
        * Test passed
    2. Check if correct form and with all fields as wanted is displayed. Check if correct ad as expected fields are displayed.
        * Test failed:
            -   I excpect that Ingredient field will be displayed as list to easly style it in line. I also expect to have object ingredient which will have 3 items (name, amount and measure). I got Ingredient-0-name, ingredient-0-amount, ingredient-0-measure, and numbers are grow.
                *  Fix: I find that i can loop thru the list items in form.ingredients and display each in seperate html element. I use it to display ingredients fields in responsive columns and in effect i can have all in one line on big screens or/and name in one line + amount and measure in second line in small screens.
            -   I have the same issue and same fix for preparation steps field.
        *   2nd test passed.
4. insert_recipe
    1.  Try to add new recipe with default fields (3 ingredient fields, 1 preparation field)
        *   Test passed.
    2.  Try to add new recipe with additional fields.
        *   Test passed.
    3.  Try to insert recipe with empty fields.
        *   Test passed - is not possible to add empty fields (except the description which has optional validator)
    4.  Insert recipe with name already used.
        *   Test passed.
5. single_recipe
    1.  Click on recipe link in home page to see if is opening as new page.
        *   Test failed - error, cannot build link as there is not variable contactForm;
            -   contact form is in base.html, so is needed in all extesnsions of base.html -  add variable to all routes which are extension of the base.html
        *   2nd test passed.
    2.  Try to open recipe with the same name as other.
        *   Test failed - instead of the clicked recipe is opened the first recipe with the same name.
            -   fix by change the variable recipe_name to recipe_id and find recipe by id in database.
        *   2nd test passed.
6. delete_recipe
    1.  Go to single recipe page and try to delete one, by click on Remove recipe.
        *   Test passed, home page displayed and flash message shows that recipe is removed.
    2.  Check if all recipe data is removed - go to mongoDB and check the collection.
        *   Test passed in 80% - all data is removed from database, but file with image still exist.
            -   Fix: add function to remove file.
        *   2nd Test passed.
7. edit_recipe
    1.  Go to single recipe page and click on edit button.
        *   Link work form for editing recipe displayed.
    2.  Check if all data is populated correctly to the form.
        *   Test failed - the way which i use to display ingredient fields in add_recipe page doesn't work here.
            -   Fix: populate data manually in edit_recipe page - instead of using {{form.ingredients}} use the html displayed by the {{form.ingredients}} - <input....>
        *   2nd Test failed - all text and number data is populated, but all data which is an option in select input are incorrect.
            -   Fix: I couldn't find better way to do it, than insert one more select option with the data from database. In effect i have doubled value which was selected:
                - example: If meal type is Warm meals, then in meal type option i have selected Warm meals and in options to select i have again Warm meals. I think that this is still good solution.
        *   3rd test failed - the meal image is not populated to file input and either to preview.
            -   fix: add image to the image preview.
8. update_recipe
    1.  Edit recipe name, recipe description, edit ingredients name, amount and measure, edit preparation steps and click update. Check if data is changed.
        *   Test passed - all data is changed correctly.
    2.  Add new ingredient, add new preparation step and click on update recipe button. Check if new data is added to recipe.
        *   Test failed - new data is added, but is not displayed correctly. New preparation step is displayed as should be. New ingredient were added to database in different direction - in database first is amount, then measure and name as last. In effect in single recipe page the list with ingredient doesn't display information correctly.
            -   Try to fix by changing the way of displaying information. 
    3.  Remove ingredient and preparation step and click update button. Check if data is removed from recipe.
        *   Test failed - removed data is still in database.
            -   Fix: change the update_one function to replace_one
            -   Fix is resolving the 3rd and 2nd issue.
        *   2nd Test failed-  error no 'meal_image' value in recipe object.
            - Fix: add manually the meal_image to recipe to make quick fix to have displayed recipe.
            - Try to remove ingredients and preparation steps, update image by click on insert image picture to test ingredients first and leave image for later test.
        *   3rd test passed - removed ingredients and preparation steps are not visible in recipe anymore.
    4.  Test if not updated image is in recipe object after update recipe - click on update recipe button in single recipe page, don't insert image and click on update recipe button.
        *   Test failed - recipe object has no meal_image value.
            -   Fix: add to update function if statement to see if new file is added, if there is not new file, then rewrite meal_image value from the first recipe object.
            -   Test by update recipe without meal_image.
        *   2nd test passed - image were not updated, but image exist in recipe object.
    5.  Test if meal_image can be updated - click on update recipe button, click on insert image button, click on update recipe button.
        *   Test passed in 40% - new image is uploaded and is visible in recipe object, is visible in home page and recipe page, but old image still exist and in edit recipe page when click on insert image, image is not visible in image preview square.
            -   Fix 1: Adjust js function to instead of set src in preview img, first check if src exist and clear before setting new value.
            -   Fix 2: add to update recipe python route, function to remove old picture in case new is not selected.
        *   2nd test passed 
9. contact
    1.  Fill in contact form and click on send button.
        *   Test passed.
10. send_mail_recipe
    1.  fill in the email address in single recipe page and click on send button; check if recipe is received on email.
        *   Test passed.
11. pdf_template
    1.  In single recipe page click on download pdf button
        *   Test failed - no 'b' in wkhtmltopdf error
            -   i try several solutions on this issue which i find in web, but none works. In end i hide the button and leave only print as there is possibility to instead of print save as pdf.
12. handle_bad_request
    1.  Try to write in web address https://cdins-msp3-recipe-book.herokuapp.com/home/anything to see if error.html page is displayed.
        *   Test passed.

### End test

1.  Add new recipe.
    * Test passed
2.  Update recipe with image, without image, by removing fields, by adding fields, by changing fields.
    * All tests passed.
3.  Remove recipe from database.
    * Test passed.
4.  Check all endpoints by clicking on different links in different pages.
    * Test passed.

## Deployment

I use github to keep my repository remotly. I use VSCode to writing the code and i deploy page on heroku srvice. To do this i did below steps:
1. Create reopsitory on github.
2. Clone repository from github to my local machine by VSCode terminal
3. Create first files, add these by command 'git add', then commit by command 'git commit' and push to github repository by typing 'git push' in terminal.
4. Create app. py file with flask logic to display "Welcome World" in webbrowser.
5. login to heroku in VSCode terminal.
6. Create heroku application.
7. add the heroku remote with repository by typing in terminal: heroku git: remote -a cdins-msp3-recipe-book
8. Create requirements.txt file by typing in terminal 'pip3 freeze > requirements.txt'
9. Create Procfile by typing in terminal: 'web: python3 app. py > Procfile'
10. Add and push created files to repository by commands: 'git add', 'git commit', 'git push' for github and 'git push heroku master' for heroku.
11. Repeat step 11 after all changes maken in code.

Website is hosted in heroku - [RecipeBook](https://cdins-msp3-recipe-book.herokuapp.com/)

### To run this project locally, follow below steps:

1. Open my Github Repository [RecipeBook - github Repo](https://github.com/dejvoss/cdins-msp3-recipe-book)
2. Click on green Code button to clone or download repository.
3. If you clone repository then copy link.
4. Open bash terminal and move to the directory to which you want clone repository.
5. Type 'git clone' and paste the copied link.
6. In main Repository folder create env. py file.
7. Add below configuration variables to the env. py file:
    * os.environ["MONGO_URI"]= "place here your Mongo DB URI" - needed for manipulating database
    * os.environ['SECRET_KEY']= "place here your SECRET KEY" - needed for forms in webpage
    * os.environ['MAIL_USERNAME']='your email username' - needed for sending contact message and sending recipe to email
    * os.environ['MAIL_DEFAULT_SENDER']='your sender email' - needed for sending contact message and sending recipe to email
    * os.environ['MAIL_PASSWORD']='your email password' - needed for sending contact message and sending recipe to email
8. In app. py file set below variables:
    * app.config["MONGO_DBNAME"] = 'name_of_collection' - type name of database collection where the recipes will be stored.     

## Credits

### Content

* Recipes was taken from private collection of my mother and sister. 

### Media

* Main video and pictures was taken from [Stock?Photo](https://shop.stockphotosecrets.com/)
* Meal images were find in web

### Support and advises

* Thanks to my mentor Reuben for support, patient, time and advises. Especially the design advices after which my page looks much better.
* Thanks to my sister for testing and inserting recipes to page.
* Thanks to my wife for support, advice and testing visual part of the web.
* Thanks to code institute to give me possibility to postponed the project submission date.