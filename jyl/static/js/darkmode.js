// Page loads with a crossed out icon, get that element and set it to none
document.getElementById("ban").style.display = "none";

// Check if user has a saved preference, if not find their computer requested preference
function isDarkModeEnabled() {
    // Check local storage for saved site theme
    const siteThemeFromStorage = window.localStorage.getItem("site-theme");
    // Return true if darkmode should be enabled
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches && (siteThemeFromStorage !== "light")) || siteThemeFromStorage === "dark";
}

// Check if user prefers darkmode
let isDarkModePreferred = isDarkModeEnabled();

// Switch theme or set theme of page
function switchTheme(theme) {
    // Darkmode
    if (theme === "dark") {

        // Set local storage to dark
        document.documentElement.setAttribute("site-theme", "dark");
        window.localStorage.setItem("site-theme", "dark");

        // Remove light class from all elements
        var all = document.getElementsByTagName("*");
        for (var i=0, max=all.length; i < max; i++) {
            if (all[i] != null) {
                var str = String(all[i].className)

                // If element has light class remove it
                if (str.substring(str.length - 5, str.length) == 'light'){
                    all[i].className = str.substring(0, str.length - 6);
                }
            }
        }

    // Lightmode
    } else {

        // Set local storage to light
        document.documentElement.setAttribute("site-theme", "light");
        window.localStorage.setItem("site-theme", "light");

        // Add light class to all elements
        var all = document.getElementsByTagName("*");
        for (var i=0, max=all.length; i < max; i++) {
            all[i].className += " light";
        }
    }
}

// If user changes modes
function overrideTheme(button) {

    // Get text element to display opposite theme
    let item = document.getElementById("switchtext");

    // Dark mode
    if (!isDarkModePreferred) {
        isDarkModePreferred = true;

        // set text to opposite theme
        item.innerHTML = "Light Theme";

        // Show proper icon
        document.getElementById("fullmoon").style.display = "none";
        document.getElementById("partmoon").style.display = "inline-block";

        // Switch theme
        switchTheme("dark");

    // Light mode
    } else {
        isDarkModePreferred = false;

        // Set to opposite theme
        item.innerHTML = "Dark Theme";

        // Show proper icon
        document.getElementById("partmoon").style.display = "none";
        document.getElementById("fullmoon").style.display = "inline-block";

        // Switch theme
        switchTheme("light");
    }
}

// Set theme based off user preference
switchTheme(isDarkModePreferred ? "dark" : "light");

// Update icons and text of button
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

// Make button override theme onclick
themeButton.onclick = overrideTheme;
overrideTheme.bind(themeButton);