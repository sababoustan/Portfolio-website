document.addEventListener("DOMContentLoaded", function () {

    const icon = document.getElementById("search-icon");
    const form = document.getElementById("search-form");

    icon.addEventListener("click", function () {
        if (form.style.display === "" || form.style.display === "none") {
            form.style.display = "block";
        } else {
            form.style.display = "none";
        }
    });

});

