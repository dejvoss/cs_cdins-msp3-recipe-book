function scrollFunction() {
    if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
        document.getElementById("main-nav-bar").classList.remove("main-nav-def")
    } else {
        document.getElementById("main-nav-bar").classList.add("main-nav-def");
    }
}

window.onscroll = function() {
    scrollFunction()
};
if (document.getElementById("myMainVideo") != null) {
    var mainVideo = document.getElementById("myMainVideo");
    var VideoBtn = document.getElementById("myVideoBtn");
    mainVideo.addEventListener('ended', function() {
        VideoBtn.innerHTML = '<i class="medium material-icons">play_circle_filled</i>';
    })
}

// Pause and play the video, and change the button text
function myFunction() {
    if (mainVideo.paused) {
        mainVideo.play();
        VideoBtn.innerHTML = '<i class="medium material-icons">pause_circle_filled</i>';
    } else {
        mainVideo.pause();
        VideoBtn.innerHTML = '<i class="medium material-icons">play_circle_filled</i>';
    }
}
// When the user scrolls down 80px from the top of the document, resize the navbar's padding and the logo's font size

var measure_option_List = ['grams', 'decagrams', 'pieces', 'pinch', 'glasses', 'liters', 'spoons', 'tea spoons']

function addIngredientField() {
    let ingredient_counter = document.getElementById("ingredient_list").childElementCount;
    let new_ingr_nr = ingredient_counter + 1;
    let pernament_field_id = "ingredients-" + ingredient_counter + "-";
    let field_id_name = pernament_field_id + "name";
    let field_id_amount = pernament_field_id + "amount";
    let field_id_measure = pernament_field_id + "measure";
    let rowId = field_id_name + "_row"
    measureList = [('grams', 'grams'), ('decagrams', 'decagrams'), ('pieces', 'pieces'), ('pinch', 'pinch'), ('glasses', 'glasses'), ('liters', 'liters'), ('spoons', 'spoons'), ('tea spoons', 'tea spoons')]
    let measure_option_Html = ""
    for (i = 0; i < measure_option_List.length; i++) {
        let measure_name = measure_option_List[i]
        measure_option_Html += '<option value="' + measure_name + '">' + measure_name + '</option>'
    };
    let html_ingredient = '<div class="col-sm-7"><label class="form-label" for="' + field_id_name + '">Ingredient name</label><input class="form-control" id="' + field_id_name + '" name="' + field_id_name + '" required type="text"></div>';
    let html_amount = '<div class="col-6 col-sm-2"><label class="form-label" for="' + field_id_amount + '">Amount</label><input class="form-control" id="' + field_id_amount + '" min="0.5" name="' + field_id_amount + '" required step="0.5" type="number"></div>';
    let html_measure = '<div class="col-6 col-sm-3"><label class="form-label" for="' + field_id_measure + '">Measure</label><select class="form-select" id="' + field_id_measure + '" name="' + field_id_measure + '" required>' + measure_option_Html + '</select></div>';
    let html_ingr_full = html_ingredient + html_amount + html_measure; //create a variable which contain all new html code for ingredient field
    let divChildEl = document.createElement("div"); // create div element for new ingredient field
    Object.assign(divChildEl, {
        className: "row",
        id: rowId
    })
    // divChildEl.setAttribute(("class", "id"), ("id", rowId));
    divChildEl.innerHTML = html_ingr_full;
    document.getElementById("ingredient_list").appendChild(divChildEl); // add div elemenet for new ingredient field
}

function removeIngredientField(btn_parent) {
    document.getElementById("ingredient_list").lastChild.remove()
}

function addStepField() {
    let step_counter = document.getElementById("preparation_steps").childElementCount;
    let field_id = "preparation-" + step_counter + "-step"
    let html_step_field = '<label class="col-sm-2 col-form-label" for="' + field_id + '">Preparation step</label><div class="col-sm-10"><textarea class="form-control" id="' + field_id + '" name="' + field_id + '" placeholder="Type the preparation step here" required rows="4"></textarea></div>';
    document.getElementById('preparation_steps').insertAdjacentHTML('beforeend', '<div class="row mb-3">' + html_step_field + '</div>');
}

function removeStepField() {
    document.getElementById("preparation_steps").lastChild.remove()
}

function PreviewImage() {
    var oFReader = new FileReader();
    oFReader.readAsDataURL(document.getElementById("meal_image").files[0]);

    oFReader.onload = function(oFREvent) {
        document.getElementById("uploadPreview").src = oFREvent.target.result;
    };
};
/* Open when someone clicks on the span element */
function openNav() {
    document.getElementById("mobile_nav").style.width = "100%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("mobile_nav").style.width = "0%";
}

/* Change the active link color in midle nav bar in home webpage source- https://www.w3schools.com/howto/howto_js_active_element.asp*/

var btnContainer = document.getElementById("middle-nav-bar");

// // Get all buttons with class="btn" inside the container
var btns = btnContainer.getElementsByClassName("midl-nav-link");
console.log(btns)
// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("midl-nav-active");
    current[0].className = current[0].className.replace(" midl-nav-active", "");
    this.className += " midl-nav-active";
  });
}
// Print recipe - open new window only with recipe content, nothing else
function printRecipe() {
   var printContent = document.getElementById("recipe-area").innerHTML;
    var printWindow = window.open("","","width=900,height=650");
    printWindow.document.write(printContent);
    printWindow.document.close();
    printWindow.print();
}
