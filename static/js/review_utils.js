function generateStars(rating) {
    if (!rating || rating <= 0) {
        return `<span class="fs-6 text-muted">No rating yet</span>`;
    }

    if (typeof rating !== 'number') {
        return `<span class="fs-6 text-muted">Error</span>`;
    }

    let stars = "";
    for (let i = 0; i < Math.round(rating); i++) {
        stars += `<i class="bi bi-star-fill me-1 fs-5 text-warning"></i>`;
    }

    return `<div class="d-flex align-items-center">${stars}<span class="ms-2 fs-6 text-dark">(${rating.toFixed(1)}/5)</span></div>`;
}

function updateAverageRating(newRating) {
    const avgRatingElement = document.getElementById("avg-rating");
    if (avgRatingElement) {
        avgRatingElement.innerHTML = generateStars(newRating);
    }
}

function generateStarsForList(rating) {
    if (!rating || rating <= 0) {
        return `<span class="fs-6 text-muted">No rating yet</span>`;
    }

    if (typeof rating !== 'number') {
        return `<span class="fs-6 text-muted">Error</span>`;
    }

    let stars = "";
    for (let i = 0; i < Math.round(rating); i++) {
        stars += `<i class="bi bi-star-fill me-1 fs-5 text-warning"></i>`;
    }

    return `<div class="d-flex align-items-center">${stars}<span class="ms-2 fs-6 text-dark">(${rating.toFixed(1)}/5)</span></div>`;
}


function updateRatingsFromServer() {
    fetch("/update-ratings/")
        .then(response => response.json())
        .then(data => {
            data.books.forEach(book => {
                const avgRatingElement = document.getElementById(`book-rating-${book.id}`);
                if (avgRatingElement) {
                    avgRatingElement.innerHTML = generateStarsForList(book.average_rating);
                }
            });
        });
}
