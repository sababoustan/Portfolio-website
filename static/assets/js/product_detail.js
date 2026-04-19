document.addEventListener("DOMContentLoaded", () => {
        fetch(`/api/products/detail/${PRODUCT_SLUG}/`)
        .then(res => res.json())
        .then(product => {

            document.getElementById("product-image").src = product.image;
            document.getElementById("product-title").innerText = product.title;
            document.getElementById("product-description").innerHTML = product.description;
            document.getElementById("product-stock").innerText = product.stock;
            document.getElementById("product-sku").innerText = product.sku;

            const qtyInput = document.getElementById("qty-input");
            if (qtyInput) {
                qtyInput.dataset.stock = product.stock;
                qtyInput.value = 1;
            }
            console.log("QTY INPUT = ", document.getElementById("qty-input"));

            const priceBox = document.getElementById("product-price");

            if (product.discount_price) {
                priceBox.innerHTML = `
                    <span class="old-price">${product.price} تومان</span>
                    <span class="new-price">${product.discount_price} تومان</span>
                `;
            } else {
                priceBox.innerHTML = `
                    <span class="new-price">${product.price} تومان</span>
                `;
            }

            document.querySelectorAll("[data-product]").forEach(btn => {
                btn.dataset.product = product.id;
            });
            document.dispatchEvent(new Event("productLoaded"));


        });
});
