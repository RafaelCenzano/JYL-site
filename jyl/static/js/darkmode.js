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
  if (!isDarkModePreferred) {
    isDarkModePreferred = true;
    this.innerHTML = "Switch to Light Theme";
    switchTheme("dark");
  } else {
    isDarkModePreferred = false;
    this.innerHTML = "Switch to Dark Theme";
    switchTheme("light");
  }
}

switchTheme(isDarkModePreferred ? "dark" : "light");

const themeButton = document.getElementById('theme-btn');
themeButton.innerHTML = isDarkModePreferred ? "Switch to Light Theme" : "Switch to Dark Theme";
themeButton.onclick = overrideTheme;
overrideTheme.bind(themeButton);