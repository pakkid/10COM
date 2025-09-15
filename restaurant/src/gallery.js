const grid = document.getElementById('galleryGrid');
const modalEl = document.getElementById('lightboxModal');
const imgEl = document.getElementById('lightboxImage');
const titleEl = document.getElementById('lightboxTitle');
const descEl = document.getElementById('lightboxDesc');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const modal = new bootstrap.Modal(modalEl);
let items = [];
let current = 0;

init();

async function init() {
    renderSkeletons(4);
    try {
        const res = await fetch('../src/data.json', { cache: 'no-cache' });
        items = await res.json();
        renderCards(items);
        attachEvents();
    } catch (e) {
        grid.innerHTML = `<div class="col-12"><div class="alert alert-danger">Failed to load gallery.</div></div>`;
        console.error(e);
    }
}

function renderSkeletons(n) {
    grid.innerHTML = '';
    for (let i=0;i<n;i++) {
        const col = document.createElement('div');
        col.className = 'col-sm-6 col-md-4 col-lg-3';
        col.innerHTML = '<div class="skeleton"></div>';
        grid.appendChild(col);
    }
}

function renderCards(data) {
    grid.innerHTML = '';
    data.forEach((item, index) => {
        const col = document.createElement('div');
        col.className = 'col-sm-6 col-md-4 col-lg-3';
        col.innerHTML = `
            <div class="card gallery-card h-100" data-index="${index}">
                <img src="${item.image}" class="card-img-top" alt="${escapeHtml(item.alt || item.title)}">
                <div class="card-body">
                    <h6 class="card-title mb-0">${escapeHtml(item.title)}</h6>
                </div>
            </div>
        `;
        grid.appendChild(col);
    });
}

function attachEvents() {
    grid.addEventListener('click', e => {
        const card = e.target.closest('.gallery-card');
        if (!card) return;
        const idx = parseInt(card.dataset.index, 10);
        show(idx);
    });
    prevBtn.addEventListener('click', () => current > 0 && show(current - 1));
    nextBtn.addEventListener('click', () => current < items.length - 1 && show(current + 1));

    modalEl.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft' && current > 0) show(current - 1);
        if (e.key === 'ArrowRight' && current < items.length - 1) show(current + 1);
    });
    modalEl.addEventListener('shown.bs.modal', () => modalEl.focus());
}

function show(index) {
    current = index;
    const item = items[current];
    imgEl.src = item.image;
    imgEl.alt = item.alt || item.title;
    titleEl.textContent = item.title;
    const credit = item.credit ? `<br><span class="text-muted fst-italic">Credit: ${escapeHtml(item.credit)}</span>` : '';
    descEl.innerHTML = escapeHtml(item.description) + credit;
    updateButtons();
    modal.show();
}

function updateButtons() {
    prevBtn.classList.toggle('d-none', current === 0);
    nextBtn.classList.toggle('d-none', current === items.length - 1);
    prevBtn.setAttribute('aria-disabled', current === 0);
    nextBtn.setAttribute('aria-disabled', current === items.length - 1);
}

function escapeHtml(str='') {
    return str.replace(/[&<>"']/g, c => ({
        '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    }[c]));
}
