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

    const btn = e.target.closest(".qty-btn");
    if (!btn) return; 

    const productId = btn.dataset.product;
    const action = btn.classList.contains("plus") ? "increase" : "decrease";
    const stock = parseInt(btn.dataset.stock);
    const qtySpan = document.getElementById(`qty-${productId}`);
    const currentQty = parseInt(qtySpan.innerText);

    if (action === "increase" && currentQty >= stock) {
        alert("حداکثر موجودی محصول همین تعداد است");
        return; 
    }
    
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
        if (data.error === "max_stock") {
        alert(data.message);
        return;
        }
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
    })
    .catch(err => console.error("Cart update error:", err));
});


// ---------------------- Add to Cart (AJAX) from Product Page ----------------------
document.addEventListener("click", function (e) {
    const btn = e.target.closest(".add-to-cart-btn");
    if (!btn) return;

    e.preventDefault();
    if (btn.dataset.loading === "true") return;
    btn.dataset.loading = "true";

    const productId = btn.dataset.product;
    const qtyInput = document.getElementById("qty-input");
    const quantity = qtyInput ? parseInt(qtyInput.value) : 1;

    fetch(`/cart/add/${productId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: `quantity=${quantity}`
    })
    .then(res => res.json())
    .then(data => {

        const cartCount = document.querySelector("#cart-count");
        if (cartCount) {
            cartCount.innerText = data.cart_count;
        }

        btn.dataset.loading = "false";
        console.log("Product added with quantity:", quantity);
    })
    .catch(() => {
        btn.dataset.loading = "false";
    });
});
