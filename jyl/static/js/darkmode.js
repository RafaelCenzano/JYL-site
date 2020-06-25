function isDarkModeEnabled() {
    const siteThemeFromStorage = window.localStorage.getItem("site-theme");
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches && (siteThemeFromStorage !== "light")) || siteThemeFromStorage === "dark";
}

let isDarkModePreferred = isDarkModeEnabled();

function switchTheme(theme) {
    if (theme === "dark") {
        document.documentElement.setAttribute("site-theme", "dark");
        window.localStorage.setItem("site-theme", "dark");

        var all = document.body.getElementsByTagName("*");
        for (var i=0, max=all.length; i < max; i++) {
            if (all[i] != null) {
                var str = String(all[i].className)
                if (str.substring(str.length - 5, str.length) == 'light'){
                    all[i].style = "transition-duration: 1s";
                    all[i].className = str.substring(0, str.length - 6);
                }
            }
        }
        setTimeout(function(){
            for(let elem of document.body.querySelectorAll("*")){
                elem.style.transitionDuration = "";
            }
        }, 1500);
    } else {
        document.documentElement.setAttribute("site-theme", "light");
        window.localStorage.setItem("site-theme", "light");

        var all = document.body.getElementsByTagName("*");
        for (var i=0, max=all.length; i < max; i++) {
            all[i].style = "transition-duration: 1s";
            all[i].className += " light";
        }
        setTimeout(function(){
            for(let elem of document.body.querySelectorAll("*")){
                elem.style.transitionDuration = "";
            }
        }, 1500);
    }
}

function switchThemeNormal(theme) {
    if (theme === "dark") {
        document.documentElement.setAttribute("site-theme", "dark");
        window.localStorage.setItem("site-theme", "dark");

        var all = document.body.getElementsByTagName("*");
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

        var all = document.body.getElementsByTagName("*");
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
