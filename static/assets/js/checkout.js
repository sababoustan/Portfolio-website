document.addEventListener("DOMContentLoaded", function () {
    const radios = document.querySelectorAll(".address-radio");
    const btn = document.getElementById("continue-btn");

    function toggleButton() {
        const checked = document.querySelector(".address-radio:checked");
        btn.disabled = !checked;
    }

    radios.forEach(radio => {
        radio.addEventListener("change", toggleButton);
    });

    toggleButton();
});
