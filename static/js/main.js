/**
 * Luminex — Main JavaScript
 * Premium interactions and micro-animations
 */

'use strict';

// ============================================================
// DOM Ready
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initHeroSlider();
  initAlertDismiss();
  initScrollTop();
  initProductGallery();
  initNavbarScroll();
  initAnimateOnScroll();
  initSortRedirect();
  initAppleCarousels();
  initBagDropdown();
});

// ============================================================
// Mobile Navigation
// ============================================================
function initMobileNav() {
  const hamburger = document.querySelector('.navbar__hamburger');
  const overlay = document.querySelector('.navbar__mobile-overlay');
  const closeBtn = document.querySelector('.navbar__mobile-close');

  if (!hamburger || !overlay) return;

  hamburger.addEventListener('click', () => {
    overlay.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    hamburger.setAttribute('aria-expanded', 'true');
  });

  function closeNav() {
    overlay.classList.remove('is-open');
    document.body.style.overflow = '';
    hamburger.setAttribute('aria-expanded', 'false');
  }

  if (closeBtn) closeBtn.addEventListener('click', closeNav);

  // Close on outside click
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeNav();
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeNav();
  });
}

// ============================================================
// Hero Slider / Auto-rotate
// ============================================================
function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-dot');

  if (slides.length <= 1) return;

  let current = 0;
  let autoplayTimer;

  function goTo(index) {
    slides[current].style.display = 'none';
    dots[current]?.classList.remove('is-active');
    current = (index + slides.length) % slides.length;
    slides[current].style.display = 'flex';
    dots[current]?.classList.add('is-active');
  }

  // Init: show first, hide rest
  slides.forEach((s, i) => {
    s.style.display = i === 0 ? 'flex' : 'none';
  });
  dots[0]?.classList.add('is-active');

  function startAutoplay() {
    autoplayTimer = setInterval(() => goTo(current + 1), 5000);
  }

  function stopAutoplay() {
    clearInterval(autoplayTimer);
  }

  startAutoplay();

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      stopAutoplay();
      goTo(i);
      startAutoplay();
    });
  });

  // Swipe support
  const slider = document.querySelector('.hero-slider');
  if (!slider) return;
  let touchStartX = 0;
  slider.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
  slider.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) {
      stopAutoplay();
      goTo(current + (dx < 0 ? 1 : -1));
      startAutoplay();
    }
  });
}

// ============================================================
// Alert Dismiss
// ============================================================
function initAlertDismiss() {
  document.querySelectorAll('.alert__close').forEach(btn => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.alert');
      if (alert) {
        alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(20px)';
        setTimeout(() => alert.remove(), 300);
      }
    });
  });

  // Auto-dismiss after 5s
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      if (alert.isConnected) {
        alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(20px)';
        setTimeout(() => alert.remove(), 500);
      }
    }, 5000);
  });
}

// ============================================================
// Scroll to Top Button
// ============================================================
function initScrollTop() {
  const btn = document.querySelector('.scroll-top');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    btn.classList.toggle('is-visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ============================================================
// Product Gallery Thumbnails
// ============================================================
function initProductGallery() {
  const mainImg = document.querySelector('.product-gallery__main-img');
  const thumbs = document.querySelectorAll('.product-gallery__thumb');

  if (!mainImg || !thumbs.length) return;

  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      const newSrc = thumb.dataset.src;
      if (!newSrc) return;

      // Fade transition
      mainImg.style.opacity = '0';
      mainImg.style.transform = 'scale(0.97)';
      mainImg.style.transition = 'opacity 0.2s ease, transform 0.2s ease';

      setTimeout(() => {
        mainImg.src = newSrc;
        mainImg.style.opacity = '1';
        mainImg.style.transform = 'scale(1)';
      }, 200);

      // Active state
      thumbs.forEach(t => t.classList.remove('is-active'));
      thumb.classList.add('is-active');
    });
  });
}

// ============================================================
// Navbar Scroll Effect
// ============================================================
function initNavbarScroll() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  window.addEventListener('scroll', () => {
    navbar.style.background = window.scrollY > 10
      ? 'rgba(255,255,255,0.92)'
      : 'rgba(255,255,255,0.85)';
  }, { passive: true });
}

// ============================================================
// Animate on Scroll (Intersection Observer)
// ============================================================
function initAnimateOnScroll() {
  const elements = document.querySelectorAll('.product-card, .category-card, .promo-card, .section-header');

  if (!elements.length || !('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
        entry.target.classList.add('aos-animate');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  elements.forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = `opacity 0.5s ease ${i * 0.04}s, transform 0.5s ease ${i * 0.04}s`;
    observer.observe(el);
  });

  // Mark animated
  document.addEventListener('animationend', (e) => {
    if (e.target.classList.contains('aos-animate')) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'none';
    }
  });

  // Trigger visible elements
  setTimeout(() => {
    elements.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight) {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }
    });
  }, 50);
}

// ============================================================
// Sort Redirect (product list / category pages)
// ============================================================
function initSortRedirect() {
  const sortSelect = document.querySelector('.sort-select');
  if (!sortSelect) return;

  sortSelect.addEventListener('change', () => {
    const url = new URL(window.location.href);
    url.searchParams.set('sort', sortSelect.value);
    window.location.href = url.toString();
  });
}

// ============================================================
// Horizontal Apple Carousel Navigation
// ============================================================
function initAppleCarousels() {
  document.querySelectorAll('.apple-carousel-section').forEach(section => {
    const track = section.querySelector('.apple-carousel__track');
    const prevBtn = section.querySelector('.apple-carousel__btn--prev');
    const nextBtn = section.querySelector('.apple-carousel__btn--next');

    if (!track) return;

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        track.scrollBy({ left: -400, behavior: 'smooth' });
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        track.scrollBy({ left: 400, behavior: 'smooth' });
      });
    }
  });
}

// ============================================================
// Shopping Bag Flyout Popover
// ============================================================
function initBagDropdown() {
  const bagButton = document.getElementById('bag-button');
  const bagDropdown = document.getElementById('bag-dropdown');
  if (!bagButton || !bagDropdown) return;

  bagButton.addEventListener('click', (e) => {
    e.preventDefault();
    const isOpen = bagDropdown.classList.toggle('is-active');
    bagButton.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  document.addEventListener('click', (e) => {
    if (!bagButton.contains(e.target) && !bagDropdown.contains(e.target)) {
      bagDropdown.classList.remove('is-active');
      bagButton.setAttribute('aria-expanded', 'false');
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      bagDropdown.classList.remove('is-active');
      bagButton.setAttribute('aria-expanded', 'false');
    }
  });
}

