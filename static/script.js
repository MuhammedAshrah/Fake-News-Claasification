document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("newsForm");
    const loadingIndicator = document.getElementById("loading");
    const resultBox = document.getElementById("result");

    form.addEventListener("submit", function (event) {
        // Show loading animation
        loadingIndicator.style.display = "flex";
        resultBox.style.opacity = "0"; // Hide previous result smoothly
    });

    // Smoothly show results when the page reloads with new data
    if (resultBox) {
        setTimeout(() => {
            resultBox.classList.add("show");
        }, 300); // Slight delay to enhance transition effect
    }
});
