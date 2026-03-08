const toggle = document.querySelector(".navbar__toggle");
const menu = document.querySelector(".navbar__menu");

if (toggle && menu) {
  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    menu.classList.toggle("is-open");
  });
}

const currentPath = window.location.pathname.replace(/\\/g, "/");

document.querySelectorAll(".navbar__menu a").forEach((link) => {
  const linkPath = new URL(link.href).pathname.replace(/\\/g, "/");
  const isIndex = linkPath.endsWith("/index.html") || linkPath === "/";
  const currentIsIndex = currentPath.endsWith("/index.html") || currentPath === "/";
  if ((isIndex && currentIsIndex) || (!isIndex && currentPath.endsWith(linkPath))) {
    link.classList.add("is-active");
  } else {
    link.classList.remove("is-active");
  }
});

function mostrarMensaje() {
  setTimeout(() => {
    document.querySelector('.form').reset();
    document.getElementById('mensaje-exito').style.display = 'block';
  }, 500);
}



// Galwría

document.addEventListener('DOMContentLoaded', () => {
  const gallery = document.querySelector('.gallery');
  if (!gallery) return;

  const displayImg = gallery.querySelector('[data-gallery-current]');
  const displayCaption = gallery.querySelector('[data-gallery-caption]');
  const thumbs = Array.from(gallery.querySelectorAll('[data-gallery-thumb]'));
  const prevBtn = gallery.querySelector('[data-gallery-prev]');
  const nextBtn = gallery.querySelector('[data-gallery-next]');
  const strip = gallery.querySelector('.gallery__strip');

  if (!displayImg || !displayCaption || thumbs.length === 0) return;

  let currentIndex = Math.max(
    thumbs.findIndex((thumb) => thumb.classList.contains('is-active')),
    0
  );

  const updateActiveThumb = (index) => {
    thumbs.forEach((thumb, i) => {
      const isActive = i === index;
      thumb.classList.toggle('is-active', isActive);
      thumb.setAttribute('aria-selected', String(isActive));
    });
  };

  const scrollToThumb = (thumb) => {
    if (!strip) return;
    const offset =
      thumb.offsetLeft - strip.clientWidth / 2 + thumb.clientWidth / 2;
    strip.scrollTo({ left: offset, behavior: 'smooth' });
  };

  const showImage = (index) => {
    const total = thumbs.length;
    currentIndex = (index + total) % total;
    const target = thumbs[currentIndex];

    displayImg.src = target.dataset.src;
    displayImg.alt = target.dataset.alt || '';
    displayCaption.textContent = target.dataset.caption || '';
    updateActiveThumb(currentIndex);
    scrollToThumb(target);
  };

  prevBtn?.addEventListener('click', () => showImage(currentIndex - 1));
  nextBtn?.addEventListener('click', () => showImage(currentIndex + 1));

  thumbs.forEach((thumb, index) => {
    thumb.addEventListener('click', () => showImage(index));
    thumb.addEventListener('keydown', (evt) => {
      if (evt.key === 'Enter' || evt.key === ' ') {
        evt.preventDefault();
        showImage(index);
      }
    });
  });

  showImage(currentIndex);
});

