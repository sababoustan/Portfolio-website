async function loadRecommendedProducts(){

    const container = document.getElementById("recommended-products");
    if (!container) return;

    try{

        const response = await fetch("/api/recommendation/",{
            headers:{
                "Authorization":"Bearer " + localStorage.getItem("access")
            }
        });

        const products = await response.json();

            products.forEach(product => {

                const card = document.createElement("div");
                card.classList.add("product-card");

                let priceHTML = "";

                if (product.discount_price) {
                    priceHTML = `
                        <span class="old-price">${product.price} تومان</span>
                        <span class="new-price">${product.discount_price} تومان</span>
                    `;
                } else {
                    priceHTML = `
                        <span class="normal-price">${product.price} تومان</span>
                    `;
                }

                card.innerHTML = `
                    <a href="/products/${product.slug}/">
                        <img src="${product.image}" alt="${product.title}">
                    </a>

                    <div class="product-title">
                        ${product.title}
                    </div>

                    <div class="product-price">
                        ${priceHTML}
                    </div>
                `;

                container.appendChild(card);

            });

    }catch(error){
        console.log("Recommendation error:",error);
    }

}

loadRecommendedProducts();

