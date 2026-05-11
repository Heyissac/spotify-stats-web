/**
 * stats.js — Mousiké
 * Lógica específica de /stats/<time_range>.
 * Reutiliza el navbar de profile.js — misma lógica, mismo patrón.
 */

// ── Navbar scroll ─────────────────────────────────────────────

function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    const onScroll = () => {
        navbar.classList.toggle('navbar--scrolled', window.scrollY > 60);
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}

// ── Barras de géneros animadas con IntersectionObserver ───────

function initGenreBars() {
    const bars = document.querySelectorAll('.genre-row__bar-fill');
    if (!bars.length) return;

    // Respetar preferencias de accesibilidad
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        bars.forEach(bar => {
            bar.style.width = bar.dataset.width;
        });
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    // Pequeño delay extra para que el stagger de entrada de la fila
                    // termine antes de que empiece la barra
                    setTimeout(() => {
                        bar.style.width = bar.dataset.width;
                    }, i * 60);
                    observer.unobserve(bar);
                }
            });
        },
        { threshold: 0.3 }
    );

    bars.forEach(bar => observer.observe(bar));
}

// ── Logout confirmación ───────────────────────────────────────

function initLogout() {
    const btn = document.getElementById('logout-btn');
    if (!btn) return;

    btn.addEventListener('click', (e) => {
        if (!confirm('¿Cerrar sesión de Spotify?')) {
            e.preventDefault();
        }
    });
}

// ── Init ──────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initGenreBars();
    initLogout();
});