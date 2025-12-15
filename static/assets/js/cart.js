// ---------------------- Get CSRF Token ----------------------
function getCookie(name) {
    let cookieValue = null;
    let cookies = document.cookie.split(";");

    for (let c of cookies) {
        c = c.trim();
        if (c.startsWith(name + "=")) {
            cookieValue = c.substring(name.length + 1);
            break;
        }
    }
    return cookieValue;
}

// ---------------------- Update Quantity in Cart Page ----------------------
document.addEventListener("click", function (e) {

    if (e.target.classList.contains("qty-btn")) {

        let productId = e.target.dataset.product;
        let action = e.target.classList.contains("plus") ? "increase" : "decrease";

        fetch(CART_UPDATE_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: `product_id=${productId}&action=${action}`
        })
        .then(res => res.json())
        .then(data => {

            if (data.removed) {
                location.reload();
                return;
            }

            document.getElementById(`qty-${productId}`).innerText = data.quantity;
            document.getElementById(`total-${productId}`).innerText = data.item_total;
            document.getElementById("cart-total").innerText = data.cart_total;
            document.getElementById("cart-discount").innerText = data.discount;
            document.getElementById("cart-final").innerText = data.final_total;

            const cartCount = document.querySelector("#cart-count");
            if (cartCount) {
                cartCount.innerText = data.cart_count;
            }
        });
    }
});


// ---------------------- Add to Cart (AJAX) from Product Page ----------------------
document.addEventListener("click", function (e) {
    const btn = e.target.closest(".add-to-cart-btn");

    if (!btn) return;

    e.preventDefault();
    if (btn.dataset.loading === "true") return;
    btn.dataset.loading = "true";

    const productId = btn.dataset.product;

    fetch(`/cart/add/${productId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(res => res.json())
    .then(data => {

        const cartCount = document.querySelector("#cart-count");

        if (cartCount) {
            cartCount.innerText = data.cart_count;
        }

        console.log("Product added to cart!");
    });
});
