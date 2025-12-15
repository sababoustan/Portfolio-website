// ---------- Get CSRF Token ----------
function getCookie(name) {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        c = c.trim();
        if (c.startsWith(name + "=")) {
            cookieValue = c.substring(name.length + 1);
            break;
        }
    }
    return cookieValue;
}

// ---------- Add / Remove (Toggle) From Product Cards ----------
if (!window.__wishlistBound) {
    window.__wishlistBound = true;

    document.addEventListener("click", function (e) {
        const btn = e.target.closest(".add-to-wishlist");
        if (!btn) return;

        e.preventDefault();

        const id = btn.dataset.product;
        if (!id) return;

        fetch(`/cart/wishlist/toggle/${id}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(res => res.json())
        .then(data => {
            const icon = btn.querySelector("i");
            const headerCount = document.querySelector("#wishlist-count");

            if (data.status === "added") {
            icon.classList.add("active");
            } else {
                icon.classList.remove("active");
            }

            if (headerCount && data.wishlist_count !== undefined) {
                headerCount.innerText = data.wishlist_count;
            }
        });
    });
}

// ---------- Remove From Wishlist Page ----------
document.addEventListener("click", function (e) {
    const btn = e.target.closest(".remove-wishlist");
    if (!btn) return;

    e.preventDefault();

    const id = btn.dataset.id;

    fetch(`/cart/wishlist/toggle/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(res => res.json())
    .then(data => {

        if (data.status === "removed") {

            btn.closest("tr").remove();

            const headerCount = document.querySelector(".wishlist-count");
            if (headerCount && typeof data.wishlist_count !== "undefined") {
                headerCount.innerText = data.wishlist_count;
            }

            if (document.querySelectorAll("tbody tr").length === 0) {
                document.querySelector("tbody").innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center">
                            هنوز هیچ محصولی در لیست علاقه‌مندی‌ها نیست.
                        </td>
                    </tr>
                `;
            }
        }
    });
});
