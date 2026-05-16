document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("loginForm");
    if (!form) {
        console.log("Login form NOT found!");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const response = await fetch("/api/accounts/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username_or_email: document.getElementById("username_or_email").value,
                password: document.getElementById("password").value
            })
        });

        const data = await response.json();

        if (response.ok && data.access) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);

            alert("ورود موفق!");
            window.location.href = "/";
        } else {
            alert(data.detail || "اطلاعات اشتباه است.");
        }
    });

});

