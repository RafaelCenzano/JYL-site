document.querySelector("textarea").addEventListener("input", () => {
    let limit = parseInt(document.querySelector("#wordCount").textContent.split("/")[1]);
    let len = document.querySelector("textarea").textLength;
    document.querySelector("textarea").value = document.querySelector("textarea").value.substring(0, Math.min(limit, len));
    document.querySelector("#wordCount").innerHTML = `${Math.min(len, limit)}/${limit}`;
});
​
document.querySelector("#mobileMenu").addEventListener("click", () => {
    document.querySelector(".sidebar").style.animationDuration = "1.5s";
    document.querySelector("#mobileMenu").style.animationDuration = "1.5s";
}