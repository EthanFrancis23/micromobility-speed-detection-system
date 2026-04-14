const API_BASE_URL = "";
const EVENTS_ENDPOINT = "/events";

// ── State ──────────────────────────────────────────────────────────────────
let allEvents = [];
let gallery = { images: [], index: 0, label: "" };

// ── Bootstrap ──────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    loadEvents();

    document.getElementById("refreshButton")
        ?.addEventListener("click", loadEvents);

    document.getElementById("applyFilter")
        ?.addEventListener("click", applyFilters);

    document.getElementById("clearFilter")
        ?.addEventListener("click", clearFilters);

    // Gallery controls
    document.getElementById("galleryClose")
        ?.addEventListener("click", closeGallery);
    document.getElementById("galleryBackdrop")
        ?.addEventListener("click", closeGallery);
    document.getElementById("galleryPrev")
        ?.addEventListener("click", () => navigateGallery(-1));
    document.getElementById("galleryNext")
        ?.addEventListener("click", () => navigateGallery(1));

    // Keyboard navigation
    document.addEventListener("keydown", handleKeydown);
});

// ── Data Loading ───────────────────────────────────────────────────────────
async function loadEvents() {
    try {
        showLoadingState();
        const response = await fetch(`${API_BASE_URL}${EVENTS_ENDPOINT}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        allEvents = await response.json();
        updateSummaryCards(allEvents);
        renderEventsTable(allEvents);
    } catch (error) {
        console.error("Error loading events:", error);
        showErrorState("Failed to load speed events. Please check the API connection.");
    }
}

// ── Summary Cards ──────────────────────────────────────────────────────────
function updateSummaryCards(events) {
    const total      = events.length;
    const violations = events.filter(e => e.speed_mph > e.threshold_value).length;
    const avg        = total > 0
        ? (events.reduce((s, e) => s + e.speed_mph, 0) / total).toFixed(1)
        : "0.0";
    const max        = total > 0
        ? Math.max(...events.map(e => e.speed_mph)).toFixed(1)
        : "0.0";

    const vals = document.querySelectorAll(".summary-value");
    if (vals.length >= 4) {
        vals[0].textContent = total;
        vals[1].textContent = violations;
        vals[2].textContent = `${avg} mph`;
        vals[3].textContent = `${max} mph`;
    }
}

// ── Filters ────────────────────────────────────────────────────────────────
function applyFilters() {
    const loc      = document.getElementById("filterLocation")?.value.trim().toLowerCase() || "";
    const minSpeed = parseFloat(document.getElementById("filterMinSpeed")?.value) || 0;

    const filtered = allEvents.filter(e => {
        const matchLoc   = !loc || (e.location || "").toLowerCase().includes(loc);
        const matchSpeed = e.speed_mph >= minSpeed;
        return matchLoc && matchSpeed;
    });

    renderEventsTable(filtered);
}

function clearFilters() {
    const locInput   = document.getElementById("filterLocation");
    const speedInput = document.getElementById("filterMinSpeed");
    if (locInput)   locInput.value   = "";
    if (speedInput) speedInput.value = "";
    renderEventsTable(allEvents);
}

// ── Table Rendering ────────────────────────────────────────────────────────
function renderEventsTable(events) {
    const tbody = document.getElementById("eventsTableBody");
    if (!tbody) return;

    // Update event count badge
    const countEl = document.getElementById("eventsCount");
    if (countEl) {
        countEl.textContent = events.length === 1
            ? "1 event"
            : `${events.length} events`;
    }

    tbody.innerHTML = "";

    if (events.length === 0) {
        tbody.innerHTML = `
            <tr class="empty-row">
                <td colspan="7">
                    <div class="empty-state">No events match the current filters.</div>
                </td>
            </tr>
        `;
        return;
    }

    events.forEach(event => {
        const row = document.createElement("tr");

        const exceeded = event.speed_mph > event.threshold_value;

        row.innerHTML = `
            <td class="cell-id">#${event.id}</td>
            <td class="cell-timestamp">${formatDateTime(event.timestamp)}</td>
            <td class="cell-speed${exceeded ? " over-limit" : ""}">${event.speed_mph.toFixed(1)} mph</td>
            <td class="cell-threshold">${event.threshold_value.toFixed(1)} mph</td>
            <td class="cell-location">${event.location || "Unknown"}</td>
            <td>${buildImageCell(event)}</td>
            <td>${exceeded
                ? `<span class="badge-violation">⚠ Violation</span>`
                : `<span class="badge-ok">✓ OK</span>`
            }</td>
        `;

        tbody.appendChild(row);
    });

    // Attach gallery click handlers
    tbody.querySelectorAll("[data-gallery]").forEach(el => {
        el.addEventListener("click", () => {
            const paths  = JSON.parse(el.dataset.gallery);
            const label  = el.dataset.label || "Event";
            openGallery(paths, label);
        });
    });
}

// ── Image Cell Builder ─────────────────────────────────────────────────────
function buildImageCell(event) {
    const paths = event.image_paths;

    if (!paths || paths.length === 0) {
        return `<span class="no-images">No images</span>`;
    }

    const encodedPaths = JSON.stringify(paths).replace(/"/g, "&quot;");
    const label = `Event #${event.id} — ${formatDateTime(event.timestamp)}`;

    // Show up to 4 tiles in a 2×2 collage
    const tiles = paths.slice(0, 4);
    const extraCount = paths.length;

    if (tiles.length === 1) {
        // Single image — simple thumbnail
        return `
            <div class="thumb-single"
                 data-gallery="${encodedPaths}"
                 data-label="${label}"
                 role="button"
                 tabindex="0"
                 title="Click to view ${paths.length} frame${paths.length !== 1 ? "s" : ""}">
                <img src="/captures/${tiles[0]}" alt="Frame 1" loading="lazy">
            </div>
        `;
    }

    const tileHTML = tiles.map((p, i) =>
        `<img src="/captures/${p}" alt="Frame ${i + 1}" loading="lazy">`
    ).join("");

    return `
        <div class="thumb-collage"
             data-gallery="${encodedPaths}"
             data-label="${label}"
             role="button"
             tabindex="0"
             title="Click to view ${paths.length} frames">
            ${tileHTML}
            <div class="thumb-overlay">
                <span class="thumb-count">${extraCount} frames</span>
            </div>
        </div>
    `;
}

// ── Gallery Modal ──────────────────────────────────────────────────────────
function openGallery(paths, label) {
    gallery.images = paths;
    gallery.index  = 0;
    gallery.label  = label;

    document.getElementById("galleryEventLabel").textContent = label;
    buildFilmstrip(paths);
    setGalleryFrame(0);

    document.getElementById("galleryModal").classList.add("open");
    document.body.style.overflow = "hidden";
}

function closeGallery() {
    document.getElementById("galleryModal").classList.remove("open");
    document.body.style.overflow = "";
}

function navigateGallery(delta) {
    const next = gallery.index + delta;
    if (next < 0 || next >= gallery.images.length) return;
    setGalleryFrame(next);
}

function setGalleryFrame(index) {
    gallery.index = index;
    const path  = gallery.images[index];
    const img   = document.getElementById("galleryMainImage");

    img.classList.add("fading");
    setTimeout(() => {
        img.src = `/captures/${path}`;
        img.onload = () => img.classList.remove("fading");
        img.onerror = () => img.classList.remove("fading");
    }, 100);

    // Counter
    document.getElementById("galleryCounter").textContent =
        `${index + 1} / ${gallery.images.length}`;

    // Prev/Next buttons
    document.getElementById("galleryPrev").disabled = index === 0;
    document.getElementById("galleryNext").disabled = index === gallery.images.length - 1;

    // Filmstrip active state
    document.querySelectorAll(".filmstrip-item").forEach((el, i) => {
        el.classList.toggle("active", i === index);
    });

    // Scroll active filmstrip item into view
    const activeItem = document.querySelector(".filmstrip-item.active");
    activeItem?.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
}

function buildFilmstrip(paths) {
    const strip = document.getElementById("galleryFilmstrip");
    strip.innerHTML = paths.map((p, i) => `
        <div class="filmstrip-item${i === 0 ? " active" : ""}"
             data-index="${i}"
             role="button"
             tabindex="0"
             aria-label="Frame ${i + 1}">
            <img src="/captures/${p}" alt="Frame ${i + 1}" loading="lazy">
        </div>
    `).join("");

    strip.querySelectorAll(".filmstrip-item").forEach(el => {
        el.addEventListener("click", () => setGalleryFrame(Number(el.dataset.index)));
    });
}

function handleKeydown(e) {
    const modal = document.getElementById("galleryModal");
    if (!modal.classList.contains("open")) return;

    if (e.key === "ArrowLeft")  navigateGallery(-1);
    if (e.key === "ArrowRight") navigateGallery(1);
    if (e.key === "Escape")     closeGallery();
}

// ── Utilities ──────────────────────────────────────────────────────────────
function formatDateTime(timestamp) {
    const date = new Date(timestamp);
    if (isNaN(date.getTime())) return timestamp;
    return date.toLocaleString("en-US", {
        month: "short", day: "numeric", year: "numeric",
        hour: "numeric", minute: "2-digit", hour12: true
    });
}

function showLoadingState() {
    const tbody = document.getElementById("eventsTableBody");
    if (!tbody) return;
    tbody.innerHTML = `
        <tr class="loading-row">
            <td colspan="7">
                <div class="loading-indicator">
                    <div class="loading-spinner"></div>
                    <span>Loading events…</span>
                </div>
            </td>
        </tr>
    `;
    const countEl = document.getElementById("eventsCount");
    if (countEl) countEl.textContent = "";
}

function showErrorState(message) {
    const tbody = document.getElementById("eventsTableBody");
    if (!tbody) return;
    tbody.innerHTML = `
        <tr class="error-row">
            <td colspan="7">
                <div class="error-state">${message}</div>
            </td>
        </tr>
    `;
}
