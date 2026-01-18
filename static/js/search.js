let page = 1;
let loading = false;
let hasNext = true;

const container = document.getElementById("productsContainer");

function fetchProducts(reset=false) {
    if (loading || !hasNext) return;

    loading = true;
    if (reset) {
        page = 1;
        container.innerHTML = "";
        hasNext = true;
    }

    const params = new URLSearchParams({
        q: searchInput.value,
        category: categoryFilter.value,
        min_price: minPrice.value,
        max_price: maxPrice.value,
        sort: sortBy.value,
        page: page
    });

    fetch(`/api/search?${params}`)
        .then(res => res.json())
        .then(data => {
            data.products.forEach(p => {
                container.innerHTML += `
                <div class="col">
                  <div class="card h-100 shadow-sm">
                    <img src="/static/uploads/${p.image}"
                         class="card-img-top"
                         style="height:220px; object-fit:cover;">
                    <div class="card-body">
                        <h6>${p.name}</h6>
                        <strong>${p.price}</strong>
                    </div>
                  </div>
                </div>`;
            });

            hasNext = data.has_next;
            page++;
            loading = false;
        });
}

// 🔍 Live Search
["input", "change"].forEach(evt => {
    searchInput.addEventListener(evt, () => fetchProducts(true));
    categoryFilter.addEventListener(evt, () => fetchProducts(true));
    minPrice.addEventListener(evt, () => fetchProducts(true));
    maxPrice.addEventListener(evt, () => fetchProducts(true));
    sortBy.addEventListener(evt, () => fetchProducts(true));
});

// ♾ Infinite Scroll
window.addEventListener("scroll", () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
        fetchProducts();
    }
});
