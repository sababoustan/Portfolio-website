document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("registerForm");
    if (!form) {
        console.log("Register form NOT found!");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const response = await fetch("/api/accounts/register/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: document.getElementById("reg_username").value.trim(),
                email: document.getElementById("reg_email").value.trim(),
                password: document.getElementById("reg_password").value.trim(),
            }),
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);

            alert("ثبت‌نام موفق!");
            window.location.href = "/";
        } else {
            alert(Object.values(data).join("\n"));
        }
    });

});


