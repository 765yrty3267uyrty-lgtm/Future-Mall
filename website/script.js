/**
 * Future Mall - Website JavaScript
 * Handles navigation, scroll effects, and interactive features.
 */

// DOM Elements
const header = document.querySelector('.header');
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navList = document.querySelector('.nav-list');
const navLinks = document.querySelectorAll('.nav-link');
const hero = document.querySelector('.hero');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initScrollEffects();
  initSmoothScroll();
  initIntersectionObserver();
  initModuleCards();
  initThemeDetection();
});

// Navigation
function initNavigation() {
  if (!mobileMenuBtn || !navList) return;

  mobileMenuBtn.addEventListener('click', () => {
    const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
    mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
    navList.classList.toggle('active');
    document.body.style.overflow = isExpanded ? '' : 'hidden';
  });

  // Close menu when clicking a link
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
      navList.classList.remove('active');
      document.body.style.overflow = '';
    });
  });

  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!header.contains(e.target) && navList.classList.contains('active')) {
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
      navList.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  // Close menu on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navList.classList.contains('active')) {
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
      navList.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
}

// Scroll Effects
function initScrollEffects() {
  let lastScrollY = window.scrollY;
  let ticking = false;

  function onScroll() {
    const scrollY = window.scrollY;

    // Header shadow
    if (scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }

    // Hero parallax (subtle)
    if (hero) {
      const heroRect = hero.getBoundingClientRect();
      if (heroRect.bottom > 0 && heroRect.top < window.innerHeight) {
        const progress = 1 - heroRect.top / window.innerHeight;
        hero.style.backgroundPositionY = `${progress * 50}px`;
      }
    }

    lastScrollY = scrollY;
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });
}

// Smooth Scroll for anchor links
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerHeight = header.offsetHeight;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - header.offsetHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });

        // Update URL without scroll
        history.pushState(null, '', targetId);
      }
    });
  });
}

// Intersection Observer for animations
function initIntersectionObserver() {
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -50px 0px',
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe elements
  const animatedElements = document.querySelectorAll(
    '.module-card, .about-card, .da-card, .brand-item, .contact-card, .module-features li'
  );

  animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Add animation classes via CSS
const style = document.createElement('style');
style.textContent = `
  .animate-in {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
`;
document.head.appendChild(style);

// Module Card Interactions
function initModuleCards() {
  const moduleCards = document.querySelectorAll('.module-card');

  moduleCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-8px)';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });

    // Keyboard accessibility
    card.addEventListener('focusin', () => {
      card.style.transform = 'translateY(-8px)';
    });

    card.addEventListener('focusout', () => {
      card.style.transform = '';
    });
  });
}

// Theme Detection (for future dark mode toggle)
function initThemeDetection() {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

  function applyTheme(e) {
    document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
  }

  prefersDark.addEventListener('change', applyTheme);
  applyTheme(prefersDark);

  // Expose for future toggle
  window.FutureMall = window.FutureMall || {};
  window.FutureMall.getTheme = () => prefersDark.matches ? 'dark' : 'light';
}

// Utility Functions
const utils = {
  // Debounce function
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  // Throttle function
  throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  },

  // Format number with commas
  formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  },

  // Get current year
  getCurrentYear() {
    return new Date().getFullYear();
  }
};

// Update copyright year
document.addEventListener('DOMContentLoaded', () => {
  const yearElements = document.querySelectorAll('[data-year]');
  yearElements.forEach(el => {
    el.textContent = utils.getCurrentYear();
  });
});

// Export for global access
window.FutureMall = window.FutureMall || {};
window.FutureMall.utils = utils;