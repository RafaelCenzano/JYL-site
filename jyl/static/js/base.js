function countWords(text) {
    return text.length || 0;
}

function jsRequired(ta, required){
    if (countWords(ta.value) > 0){
        required.style.display = 'none';
    }else {
        if (window.matchMedia("(max-width: 900px)").matches){
            required.style.display = 'block';
        }else {
            required.style.display = 'inline-block';
        }
    }
    ta.addEventListener('input', () => {
        if (countWords(ta.value) > 0){
            required.style.display = 'none';
        }else {
            if (window.matchMedia("(max-width: 900px)").matches){
                required.style.display = 'block';
            }else {
                required.style.display = 'inline-block';
            }
        }
    });
}

function jsTextArea(ta, span, number){
    span.innerText = countWords(ta.value) + '/' + number;
    ta.addEventListener('input', () => {
        span.innerText = countWords(ta.value) + '/' + number;
        if (countWords(ta.value) > number){
            span.style.color = '#c21b1b';
        }else {
            span.style.color = '#000000';
        }
    });
}

var close = document.getElementsByClassName("closebtn");
var i;

for (i = 0; i < close.length; i++) {
close[i].onclick = function(){
    var div = this.parentElement;
        div.style.opacity = "0";
        setTimeout(function(){ div.style.display = "none"; }, 600);
    }
}

document.querySelector("#mobileMenu").addEventListener("click", () => {
    document.querySelector(".sidebar").style.animationDuration = "1.5s";
    document.querySelector("#mobileMenu").style.animationDuration = "1.5s";
});