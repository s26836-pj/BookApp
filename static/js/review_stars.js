document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll("#rating-stars i");
    const ratingInput = document.getElementById("review-rating");

    if (!stars || !ratingInput) return;

    function highlightStars(value) {
        stars.forEach(star => {
            if (star.getAttribute("data-value") <= value) {
                star.classList.add("text-warning");
                star.classList.remove("bi-star");
                star.classList.add("bi-star-fill", "me-1");
            } else {
                star.classList.remove("text-warning");
                star.classList.add("bi-star");
                star.classList.remove("bi-star-fill", "me-1");
            }
        });
    }

    stars.forEach(star => {
        star.addEventListener("mouseover", () => highlightStars(star.getAttribute("data-value")));
        star.addEventListener("click", () => {
            ratingInput.value = star.getAttribute("data-value");
            highlightStars(ratingInput.value);
        });
        star.addEventListener("mouseleave", () => highlightStars(ratingInput.value));
    });

    highlightStars(ratingInput.value);
});
