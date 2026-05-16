document.addEventListener("DOMContentLoaded", () => {
    const section = document.querySelector(".comment-section");
    if (!section) return;

    const slug = section.dataset.slug;
    const list = document.getElementById("comments-list");
    const count = document.getElementById("comments-count");
    const form = document.getElementById("comment-form");

    function renderReplies(replies) {
        if (!replies || replies.length === 0) return "";

        return replies.map(reply => `
            <div class="admin-reply">
                <strong>پاسخ مدیر</strong>
                <p>${reply.body}</p>
            </div>
        `).join("");
    }

    function loadComments() {
        fetch(`/api/comments/${slug}/`)
            .then(res => res.json())
            .then(comments => {
                count.textContent = comments.length;
                list.innerHTML = "";

                if (comments.length === 0) {
                    list.innerHTML = `<p class="no-comments">هنوز نظری ثبت نشده است.</p>`;
                    return;
                }

                comments.forEach(comment => {
                    const el = document.createElement("div");
                    el.className = "comment-card";
                    el.innerHTML = `
                        <div class="comment-header">
                            <span class="comment-user">${comment.user}</span>
                            <span class="comment-date">
                                ${new Date(comment.created_at).toLocaleDateString("fa-IR")}
                            </span>
                        </div>
                        <p class="comment-text">${comment.body}</p>
                        ${renderReplies(comment.replies)}
                    `;
                    list.appendChild(el);
                });
            });
    }
    loadComments();

    if (form) {
        form.addEventListener("submit", e => {
            e.preventDefault();

            const body = document.getElementById("comment-body").value.trim();
            if (!body) return;

            const token = localStorage.getItem("access");

            if (!token) {
                alert("برای ثبت نظر باید وارد شوید.");
                return;
            }

            fetch(`/api/comments/${slug}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ body })
            })
            .then(res => {
                if (!res.ok) throw new Error();
                return res.json();
            })
            .then(() => {
                alert("نظر شما ثبت شد.");
                form.reset();
                loadComments();
            })
            .catch(() => {
                alert("خطا در ثبت نظر.");
            });
        });
    }
});
