document.addEventListener("DOMContentLoaded", function () {

    const qtyInput = document.getElementById("qty-input");
    const errorBox = document.getElementById("qty-error");

    if (!qtyInput) return;

    const maxStock = Number(qtyInput.dataset.stock);

    function showError(msg) {
        errorBox.textContent = msg;
        errorBox.style.display = "block";
    }

    function hideError() {
        errorBox.textContent = "";
        errorBox.style.display = "none";
    }

    function getQty() {
        return Number(qtyInput.value) || 1;
    }

    function setQty(value) {
        qtyInput.value = value;
        console.log("Quantity:", value);
    }

    document.querySelectorAll(".qty-btn-product").forEach(btn => {
        btn.addEventListener("click", function () {

            let qty = getQty();
            const action = this.dataset.action;

            if (action === "plus") {
                if (qty < maxStock) {
                    setQty(qty + 1);
                    hideError();
                } else {
                    setQty(maxStock);
                    showError("حداکثر موجودی محصول همین تعداد است");
                }
            }

            if (action === "minus") {
                if (qty > 1) {
                    setQty(qty - 1);
                    hideError();
                }
            }
        });
    });

});
