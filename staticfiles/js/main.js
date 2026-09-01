/**
 * Gen-Z Constructors Limited Company - Main JavaScript
 * Mobile-first interactions, menu toggling, FAQ accordions, and gallery lightbox.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Lucide Icons if available
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // 2. Header Scroll Effect
  const header = document.querySelector('.site-header');
  if (header) {
    const handleScroll = () => {
      if (window.scrollY > 30) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // 3. Mobile Navigation Drawer
  const menuBtn = document.getElementById('mobile-menu-btn');
  const closeMenuBtn = document.getElementById('mobile-menu-close');
  const mobileDrawer = document.getElementById('mobile-drawer');
  const drawerBackdrop = document.getElementById('mobile-drawer-backdrop');

  const openDrawer = () => {
    if (mobileDrawer) {
      mobileDrawer.classList.remove('translate-x-full');
      mobileDrawer.classList.add('translate-x-0');
    }
    if (drawerBackdrop) {
      drawerBackdrop.classList.remove('hidden');
      setTimeout(() => drawerBackdrop.classList.remove('opacity-0'), 10);
    }
    document.body.style.overflow = 'hidden';
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'true');
  };

  const closeDrawer = () => {
    if (mobileDrawer) {
      mobileDrawer.classList.remove('translate-x-0');
      mobileDrawer.classList.add('translate-x-full');
    }
    if (drawerBackdrop) {
      drawerBackdrop.classList.add('opacity-0');
      setTimeout(() => drawerBackdrop.classList.add('hidden'), 300);
    }
    document.body.style.overflow = '';
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
  };

  if (menuBtn) menuBtn.addEventListener('click', openDrawer);
  if (closeMenuBtn) closeMenuBtn.addEventListener('click', closeDrawer);
  if (drawerBackdrop) drawerBackdrop.addEventListener('click', closeDrawer);

  // Close drawer on escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeDrawer();
      closeLightbox();
    }
  });

  // 4. FAQ Accordions
  const faqToggles = document.querySelectorAll('.faq-toggle');
  faqToggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
      const targetId = toggle.getAttribute('data-target');
      const targetContent = document.getElementById(targetId);
      const icon = toggle.querySelector('.faq-icon');

      if (targetContent) {
        const isHidden = targetContent.classList.contains('hidden');
        // Close other FAQs in the same group
        document.querySelectorAll('.faq-content').forEach(c => {
          if (c !== targetContent) c.classList.add('hidden');
        });
        document.querySelectorAll('.faq-icon').forEach(ic => {
          if (ic !== icon) ic.style.transform = 'rotate(0deg)';
        });

        if (isHidden) {
          targetContent.classList.remove('hidden');
          if (icon) icon.style.transform = 'rotate(180deg)';
        } else {
          targetContent.classList.add('hidden');
          if (icon) icon.style.transform = 'rotate(0deg)';
        }
      }
    });
  });

  // 5. Lightbox Modal for Gallery Images
  const galleryItems = document.querySelectorAll('[data-lightbox-src]');
  const lightbox = document.getElementById('image-lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxCaption = document.getElementById('lightbox-caption');
  const lightboxClose = document.getElementById('lightbox-close');

  const openLightbox = (src, caption) => {
    if (lightbox && lightboxImg) {
      lightboxImg.src = src;
      if (lightboxCaption) lightboxCaption.textContent = caption || '';
      lightbox.classList.remove('hidden');
      setTimeout(() => lightbox.classList.remove('opacity-0'), 10);
      document.body.style.overflow = 'hidden';
    }
  };

  const closeLightbox = () => {
    if (lightbox) {
      lightbox.classList.add('opacity-0');
      setTimeout(() => {
        lightbox.classList.add('hidden');
        if (lightboxImg) lightboxImg.src = '';
      }, 250);
      document.body.style.overflow = '';
    }
  };

  galleryItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const src = item.getAttribute('data-lightbox-src');
      const caption = item.getAttribute('data-caption') || item.getAttribute('title');
      openLightbox(src, caption);
    });
  });

  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });
  }

  // 6. Dismiss Toast Messages
  const toastDismissButtons = document.querySelectorAll('.toast-dismiss');
  toastDismissButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const toast = btn.closest('.toast-item');
      if (toast) {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        setTimeout(() => toast.remove(), 250);
      }
    });
  });

  // Auto-hide messages after 6s
  setTimeout(() => {
    document.querySelectorAll('.toast-item').forEach(toast => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      setTimeout(() => toast.remove(), 250);
    });
  }, 6000);
});
