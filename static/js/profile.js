/**
 * profile.js — Mousiké
 * Lógica específica de la página de perfil.
 */

// ── Navbar: fondo al hacer scroll ─────────────────────────────

function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  const onScroll = () => {
    navbar.classList.toggle('navbar--scrolled', window.scrollY > 60);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // Estado inicial
}

// ── Toggle "ver más" en historial reciente ────────────────────

function initRecentToggle() {
  const btn     = document.getElementById('recent-toggle');
  const btnText = document.getElementById('recent-toggle-text');
  const icon    = document.getElementById('recent-toggle-icon');
  if (!btn) return;

  const hiddenRows = document.querySelectorAll('.recent-row--hidden');
  let expanded = false;

  // Quitar display:none del CSS para manejar visibilidad con JS
  hiddenRows.forEach(row => {
    row.style.display = 'none';
    row.classList.remove('recent-row--hidden');
  });

  btn.addEventListener('click', () => {
    expanded = !expanded;
    btn.setAttribute('aria-expanded', String(expanded));

    hiddenRows.forEach((row, i) => {
      if (expanded) {
        row.style.display = '';
        // Stagger de entrada
        row.style.opacity = '0';
        row.style.transform = 'translateY(10px)';
        row.style.transition = 'none';

        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            row.style.transition = `opacity 300ms ${i * 45}ms var(--ease-out), transform 300ms ${i * 45}ms var(--ease-out)`;
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
          });
        });
      } else {
        row.style.transition = `opacity 200ms ease, transform 200ms ease`;
        row.style.opacity = '0';
        row.style.transform = 'translateY(6px)';
        setTimeout(() => { row.style.display = 'none'; }, 220);
      }
    });

    btnText.textContent = expanded ? 'Ver menos' : 'Ver más';
    icon.classList.toggle('recent-toggle__icon--rotated', expanded);
  });
}

// ── Logout: confirmación simple ───────────────────────────────

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
  initRecentToggle();
  initLogout();
});