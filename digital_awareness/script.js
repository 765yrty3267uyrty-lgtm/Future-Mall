/**
 * Future Mall - Digital Awareness JavaScript
 * Handles navigation, interactive features, and animations.
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initScrollEffects();
  initSmoothScroll();
  initIntersectionObserver();
  initInteractiveFeatures();
});

// Navigation
function initNavigation() {
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const navList = document.querySelector('.nav-list');

  if (!mobileMenuBtn || !navList) return;

  mobileMenuBtn.addEventListener('click', () => {
    const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
    mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
    navList.classList.toggle('active');
    document.body.style.overflow = isExpanded ? '' : 'hidden';
  });

  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
      navList.classList.remove('active');
      document.body.style.overflow = '';
    });
  });

  document.addEventListener('click', (e) => {
    const header = document.querySelector('.header');
    if (!header.contains(e.target) && navList.classList.contains('active')) {
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
      navList.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

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
  const header = document.querySelector('.header');
  let ticking = false;

  function onScroll() {
    const scrollY = window.scrollY;
    if (scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });
}

// Smooth Scroll
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerHeight = document.querySelector('.header').offsetHeight;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });

        history.pushState(null, '', targetId);
      }
    });
  });
}

// Intersection Observer for animations
function initIntersectionObserver() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, {
    rootMargin: '0px 0px -50px 0px',
    threshold: 0.1
  });

  const animatedElements = document.querySelectorAll(
    '.module-card, .tip-card, .cta-card, .stat-item'
  );

  animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Interactive Features
function initInteractiveFeatures() {
  // Module card hover effects
  document.querySelectorAll('.module-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-8px)';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });

    card.addEventListener('focusin', () => {
      card.style.transform = 'translateY(-8px)';
    });

    card.addEventListener('focusout', () => {
      card.style.transform = '';
    });
  });

  // Tip card hover
  document.querySelectorAll('.tip-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-8px)';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });

  // Stat item hover
  document.querySelectorAll('.stat-item').forEach(item => {
    item.addEventListener('mouseenter', () => {
      item.style.transform = 'translateY(-6px)';
    });

    item.addEventListener('mouseleave', () => {
      item.style.transform = '';
    });
  });

  // Keyboard accessibility
  document.querySelectorAll('.module-card, .tip-card, .stat-item').forEach(el => {
    el.addEventListener('focusin', () => {
      el.style.transform = 'translateY(-8px)';
    });

    el.addEventListener('focusout', () => {
      el.style.transform = '';
    });
  });
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
  .animate-in {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
`;
document.head.appendChild(style);