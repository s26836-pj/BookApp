document.addEventListener("DOMContentLoaded", function () {
    const confirmDeleteBtn = document.getElementById("confirmDeleteReview");
    const deleteModalElement = document.getElementById("deleteReviewModal");

    function attachDeleteEvent(button) {
        if (!button) return;
        button.addEventListener("click", function () {
            const reviewId = this.getAttribute("data-review-id");
            const csrfToken = this.getAttribute("data-csrf-token");

            confirmDeleteBtn.setAttribute("data-review-id", reviewId);
            confirmDeleteBtn.setAttribute("data-csrf-token", csrfToken);

            const deleteModal = new bootstrap.Modal(deleteModalElement);
            deleteModal.show();
        });
    }

    confirmDeleteBtn.addEventListener("click", function () {
        const reviewId = this.getAttribute("data-review-id");
        const csrfToken = this.getAttribute("data-csrf-token");

        const deleteModal = bootstrap.Modal.getInstance(deleteModalElement);
        deleteModal.hide();

        fetch(`/review/delete/${reviewId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const reviewElement = document.getElementById(`review-${reviewId}`);
                    if (reviewElement) {
                        reviewElement.remove();
                    }

                    const remaining = document.querySelectorAll("#review-list .border-bottom").length;
                    updateAverageRating(remaining === 0 ? 0 : data.new_avg_rating);
                }
            });
    });

    document.querySelectorAll(".delete-review-btn").forEach(button => {
        attachDeleteEvent(button);
    });

    window.attachDeleteEvent = attachDeleteEvent;
});
