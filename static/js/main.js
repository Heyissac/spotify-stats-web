/**
 * main.js — Mousiké
 * Módulo ES6: se carga con type="module", sin dependencias externas.
 */

// ── Animaciones de entrada con IntersectionObserver ───────────────

function initScrollAnimations() {
    if (!('IntersectionObserver' in window)) {
        // Fallback: mostrar todo sin animación
        document.querySelectorAll('[data-animate]').forEach(el => {
            el.classList.add('is-visible');
        });
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    document.querySelectorAll('[data-animate]').forEach(el => observer.observe(el));
}

// ── Texto rotatorio del hero ──────────────────────────────────────

function initRotatingSubtitle() {
    const el = document.getElementById('hero-subtitle');
    if (!el) return;

    const phrases = [
        'Explora tus <strong>canciones favoritas</strong>, artistas más escuchados y géneros musicales preferidos.',
        'Obtén <strong>insights detallados</strong> sobre tus hábitos de escucha con análisis por períodos de tiempo.',
        'Descubre tu <strong>evolución musical</strong> a lo largo de semanas, meses y años.',
        'Conoce las <strong>estadísticas completas</strong> de tu biblioteca musical personalizada.',
        '¿Qué has estado escuchando? <strong>Revive tu historial</strong> reciente al detalle.',
    ];

    let current = 0;

    function rotate() {
        // Fade out
        el.style.opacity = '0';
        el.style.transform = 'translateY(-8px)';

        setTimeout(() => {
            current = (current + 1) % phrases.length;
            el.innerHTML = phrases[current];

            // Fade in
            requestAnimationFrame(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            });
        }, 450);
    }

    // La primera frase ya está en el HTML; rotar a partir de la segunda
    setInterval(rotate, 5000);
}

// ── Init ──────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initScrollAnimations();
    initRotatingSubtitle();
});