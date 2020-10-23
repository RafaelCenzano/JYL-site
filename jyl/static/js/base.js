// Return character count
function countWords(text) {
    return text.length || 0;
}

// Use js to show and hide "*required" tag on forms
function jsRequired(ta, required){
    // Do check first in case form is pre-filled with data
    // Hide required if form has data
    if (countWords(ta.value) > 0){
        required.style.display = 'none';

    // Make required reappear
    } else {
        if (window.matchMedia("(max-width: 900px)").matches){
            required.style.display = 'block';
        } else {
            required.style.display = 'inline-block';
        }
    }

    // Set event listener to check if form field has data
    ta.addEventListener('input', () => {

        // Hide required if form has data
        if (countWords(ta.value) > 0){
            required.style.display = 'none';

        // Make required reappear
        } else {
            if (window.matchMedia("(max-width: 900px)").matches){
                required.style.display = 'block';
            } else {
                required.style.display = 'inline-block';
            }
        }
    });
}

// Use js to show current wordcount for textarea
function jsTextArea(ta, span, number){

    // Set text to current character count / maximum
    span.innerText = countWords(ta.value) + '/' + number;

    // Create event listener to update character count as text area is manipulated
    ta.addEventListener('input', () => {

        // Set element text
        span.innerText = countWords(ta.value) + '/' + number;

        // Update color to red if character count goes over maximum
        if (countWords(ta.value) > number){
            span.style.color = '#c21b1b';

        // Else set color to proper color for theme color
        } else {
            if (window.localStorage.getItem("site-theme") == "dark"){
                span.style.color = '#ddd';
            } else {
                span.style.color = '#000';
            }
        }
    });
}

// Get closebtn if it exsists
var close = document.getElementsByClassName("closebtn");

// Update each close button found
for (var i = 0; i < close.length; i++) {
    close[i].onclick = function(){
        var div = this.parentElement;
        div.style.opacity = "0";
        setTimeout(function(){ div.style.display = "none"; }, 600);
    }
}

// Use js to fix bug with sidebar and sidebar transitions
document.querySelector("#mobileMenu").addEventListener("click", () => {
    document.querySelector(".sidebar").style.animationDuration = "1.5s";
    document.querySelector("#mobileMenu").style.animationDuration = "1.5s";
});