document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.getElementById("wishlist-table-body");
    const wishlistCountElement = document.querySelector("#wishlist-count");
    const token = localStorage.getItem("access");
    function updateWishlistCount(count) {
        if (wishlistCountElement) {
            wishlistCountElement.innerText = count !== undefined ? count : 0;
        }
    }
    function loadWishlist() {
        if (!tableBody) return;

        if (!token) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center">
                        لطفاً ابتدا <a href="/login/">وارد شوید</a>.
                    </td>
                </tr>
            `;
            updateWishlistCount(0);
            return;
        }

        fetch("/api/cart/wishlist/", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            tableBody.innerHTML = "";

            if (!data || data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center">
                            هنوز هیچ محصولی در لیست علاقه‌مندی‌ها نیست.
                        </td>
                    </tr>
                `;
                updateWishlistCount(0);
                return;
            }

            data.forEach(item => {
                const product = item.product || {};
                const imageUrl = product.image || "/static/assets/img/placeholder.jpg";
                const title = product.title || "بدون نام";
                const price = product.price
                    ? product.price.toLocaleString("fa-IR") + " تومان"
                    : "—";
                const row = `
                    <tr>
                        <td class="product-name">
                            <div class="wishlist-product-box">
                                <img src="${imageUrl}" class="wishlist-product-img" alt="${title}">
                                <div>
                                    <div class="wishlist-product-title">${title}</div>
                                    <small class="d-block text-muted">
                                        اضافه شده در: ${new Date(item.added_at).toLocaleDateString("fa-IR")}
                                    </small>
                                </div>
                            </div>
                        </td>
                        <td class="product-price">
                            <span class="amount">${price}</span>
                        </td>
                        <td class="product-remove">
                            <a href="#" class="remove-wishlist" data-id="${product.id}">
                                <i class="fa fa-times"></i>
                            </a>
                        </td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML("beforeend", row);
            });
            updateWishlistCount(data.length);
        })
        .catch(err => {
            console.error("Wishlist loading error:", err);
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center text-danger">
                        خطا در ارتباط با سرور.
                    </td>
                </tr>
            `;
            updateWishlistCount(0);
        });
    }
    document.addEventListener("click", function (e) {
        const btn = e.target.closest(".remove-wishlist");
        if (!btn) return;

        e.preventDefault();

        const id = btn.dataset.id;

        fetch(`/api/cart/wishlist/toggle/${id}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "removed") {
                const row = btn.closest("tr");
                if (row) row.remove();
                updateWishlistCount(data.wishlist_count);
                if (tableBody.querySelectorAll("tr").length === 0) {
                    tableBody.innerHTML = `
                        <tr>
                            <td colspan="4" class="text-center">
                                هنوز هیچ محصولی در لیست علاقه‌مندی‌ها نیست.
                            </td>
                        </tr>
                    `;
                }
            } else {
                alert("خطا در حذف آیتم از لیست علاقه‌مندی‌ها");
            }
        })
        .catch(err => {
            console.error("Wishlist remove error:", err);
            alert("خطا در ارتباط با سرور هنگام حذف.");
        });
    });
    document.addEventListener("click", function (e) {
        const btn = e.target.closest(".add-to-wishlist");
        if (!btn) return;

        e.preventDefault();

        const id = btn.dataset.product;

        fetch(`/api/cart/wishlist/toggle/${id}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            }
        })
        .then(r => r.json())
        .then(data => {
            const icon = btn.querySelector("i");
            if (icon) {
                if (data.status === "added") {
                    icon.classList.add("active");
                } else {
                    icon.classList.remove("active");
                }
            }
            updateWishlistCount(data.wishlist_count);
            if (data.status === "removed") {
                const rowToRemove = document.querySelector(`a[data-id="${id}"]`)?.closest('tr');
                if (rowToRemove) {
                    rowToRemove.remove();
                    if (tableBody && tableBody.querySelectorAll("tr").length === 0) {
                        tableBody.innerHTML = `
                            <tr>
                                <td colspan="4" class="text-center">
                                    هنوز هیچ محصولی در لیست علاقه‌مندی‌ها نیست.
                                </td>
                            </tr>
                        `;
                    }
                }
            }

        })
        .catch(err => {
            console.error("Toggle wishlist error:", err);
            alert("خطا در افزودن/حذف از لیست علاقه‌مندی‌ها.");
        });
    });
    loadWishlist();

});


