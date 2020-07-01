document.getElementById("ban").style.display = "none";

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

function overrideTheme(button) {
    let item = document.getElementById("switchtext");

    if (!isDarkModePreferred) {
        isDarkModePreferred = true;
        item.innerHTML = "Light Theme";
        document.getElementById("fullmoon").style.display = "none";
        document.getElementById("partmoon").style.display = "inline-block";
        switchTheme("dark");
    } else {
        isDarkModePreferred = false;
        item.innerHTML = "Dark Theme";
        document.getElementById("partmoon").style.display = "none";
        document.getElementById("fullmoon").style.display = "inline-block";
        switchTheme("light");
    }
}

switchTheme(isDarkModePreferred ? "dark" : "light");

const themeButton = document.getElementById('theme-btn');
let item = document.getElementById("switchtext");
if (isDarkModePreferred) {
    item.innerHTML = "Light Theme";
    document.getElementById("fullmoon").style.display = "none";
    document.getElementById("partmoon").style.display = "inline-block";
} else {
    item.innerHTML = "Dark Theme";
    document.getElementById("partmoon").style.display = "none";
    document.getElementById("fullmoon").style.display = "inline-block";
}
themeButton.onclick = overrideTheme;
overrideTheme.bind(themeButton);