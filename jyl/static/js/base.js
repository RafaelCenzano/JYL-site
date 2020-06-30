function isDarkModeEnabled() {
    const siteThemeFromStorage = window.localStorage.getItem("site-theme");
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches && (siteThemeFromStorage !== "light")) || siteThemeFromStorage === "dark";
}

let isDarkModePreferred = isDarkModeEnabled();

function switchTheme(theme) {
    if (theme === "dark") {
        document.documentElement.setAttribute("site-theme", "dark");
        window.localStorage.setItem("site-theme", "dark");

        var all = document.getElementsByTagName("*");
        for (var i=0, max=all.length; i < max; i++) {
            if (all[i] != null) {
                var str = String(all[i].className)
                if (str.substring(str.length - 5, str.length) == 'light'){
                    all[i].className = str.substring(0, str.length - 6);
                }
            }
        }
    } else {
        document.documentElement.setAttribute("site-theme", "light");
        window.localStorage.setItem("site-theme", "light");

        var all = document.getElementsByTagName("*");
        for (var i=0, max=all.length; i < max; i++) {
            all[i].className += " light";
        }
    }
}

function switchThemeNormal(theme) {
    if (theme === "dark") {
        document.documentElement.setAttribute("site-theme", "dark");
        window.localStorage.setItem("site-theme", "dark");

        var all = document.getElementsByTagName("*");
        for (var i=0, max=all.length; i < max; i++) {
            if (all[i] != null) {
                var str = String(all[i].className)
                if (str.substring(str.length - 5, str.length) == 'light'){
                    all[i].className = str.substring(0, str.length - 6);
                }
            }
        }
    } else {
        document.documentElement.setAttribute("site-theme", "light");
        window.localStorage.setItem("site-theme", "light");

        var all = document.getElementsByTagName("*");
        for (var i=0, max=all.length; i < max; i++) {
            all[i].className += " light";
        }
    }
}

function overrideTheme(button) {
    let item = document.getElementById("switchtext");
    let icon = document.getElementById("icon");

    if (!isDarkModePreferred) {
        isDarkModePreferred = true;
        item.innerHTML = "Light Theme";
        icon.className = "far fa-moon";
        switchTheme("dark");
    } else {
        isDarkModePreferred = false;
        item.innerHTML = "Dark Theme";
        icon.className = "fas fa-moon";
        switchTheme("light");
    }
}

switchThemeNormal(isDarkModePreferred ? "dark" : "light");

const themeButton = document.getElementById('theme-btn');
let item = document.getElementById("switchtext");
let icon = document.getElementById("icon");
if (isDarkModePreferred) {
    item.innerHTML = "Light Theme";
    icon.className = "far fa-moon";
} else {
    item.innerHTML = "Dark Theme";
    icon.className = "fas fa-moon";
}
themeButton.onclick = overrideTheme;
overrideTheme.bind(themeButton);


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
            if (window.localStorage.getItem("site-theme") == "dark"){
                span.style.color = '#ddd';
            }else {
                span.style.color = '#000';
            }
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