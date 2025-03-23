function getActiveFilters() {
    const params = new URLSearchParams();
    const category = document.getElementById("category-filter").value;
    if (category) params.append("category", category);
    return params;
}

function applyFilters(page = 1) {
    const params = getActiveFilters();
    params.append("page", page);
    window.history.pushState({}, "", "?" + params.toString());
    fetch(`/filter-books/?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("book-container").innerHTML = data.html;
            attachPaginationEvents();
        })
}

function attachPaginationEvents() {
    const links = document.querySelectorAll(".page-link");
    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const page = this.getAttribute("data-page");
            if (page) {
                applyFilters(page);
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const categoryFilter = document.getElementById("category-filter");
    categoryFilter.addEventListener("change", () => applyFilters());
    attachPaginationEvents();
});