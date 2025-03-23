document.addEventListener("DOMContentLoaded", function () {
    const reviewForm = document.getElementById("review-form");

    if (!reviewForm) return;

    const ratingInput = document.getElementById("review-rating");
    const reviewUrl = reviewForm.dataset.url || window.location.href;


    function escapeHTML(str) {
        const div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    reviewForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(reviewForm);

        fetch(reviewUrl, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
            .then(response => response.json())
            .then(data => {

                const errorContainer = document.getElementById("review-error");

                if (data.success) {
                    if (errorContainer) {
                        errorContainer.classList.add("d-none");
                        errorContainer.innerText = "";
                    }

                    const reviewList = document.getElementById("review-list");
                    if (!reviewList) return;

                    const newReview = document.createElement("div");
                    newReview.classList.add("border-bottom", "mb-3", "pb-2");
                    newReview.setAttribute("id", `review-${data.review_id}`);

                    const rating = parseInt(data.rating);

                    newReview.innerHTML = `
                        <p><strong>${data.user}</strong></p>
                        <p>${escapeHTML(data.content)}</p>
                        ${generateStars(rating)}
                        ${USER_IS_ADMIN ? `
                        <button class="btn btn-sm btn-outline-danger delete-review-btn"
                            data-review-id="${data.review_id}"
                            data-csrf-token="${document.querySelector("[name=csrfmiddlewaretoken]").value}">
                            Delete
                        </button>
                        `: ""}
                    `;

                    reviewList.appendChild(newReview);
                    updateAverageRating(data.new_avg_rating);
                    attachDeleteEvent(newReview.querySelector(".delete-review-btn"));

                    reviewForm.reset();
                    ratingInput.value = 0;
                    highlightStars(0);

                } else {
                    if (errorContainer) {
                        if (typeof data.error === "object") {
                            const allErrors = [];

                            for (const field in data.error) {
                                const messages = data.error[field];
                                messages.forEach(msg => {
                                    if (typeof msg === "string") {
                                        allErrors.push(msg);
                                    } else if (typeof msg === "object" && msg.message) {
                                        allErrors.push(msg.message);
                                    } else {
                                        allErrors.push(JSON.stringify(msg));
                                    }
                                });
                            }

                            errorContainer.innerText = allErrors.join(" ");
                        }
                        errorContainer.classList.remove("d-none");

                        setTimeout(() => {
                            errorContainer.classList.add("d-none");
                            errorContainer.innerText = "";
                        }, 5000);
                    }
                }
            })
            .catch(() => {
                const errorContainer = document.getElementById("review-error");
                if (errorContainer) {
                    errorContainer.classList.remove("d-none");

                    setTimeout(() => {
                        errorContainer.classList.add("d-none");
                        errorContainer.innerText = "";
                    }, 5000);
                }
            });
    });
});
