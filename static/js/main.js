// AI Band Generator - Retro 90s JS
// Minimal — just enough to keep things working

document.addEventListener('DOMContentLoaded', function() {
    // Respect prefers-reduced-motion: skip purely-cosmetic animations.
    var prefersReducedMotion = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
        return;
    }

    // Add a subtle star twinkle effect to the starfield background
    // (purely cosmetic, non-blocking)
    try {
        var stars = document.querySelectorAll('.banner-stars');
        if (stars.length > 0) {
            setInterval(function() {
                stars.forEach(function(el) {
                    el.style.opacity = (Math.random() * 0.4 + 0.6).toFixed(2);
                });
            }, 2000);
        }
    } catch(e) {
        // Silently ignore — cosmetic only
    }
});
