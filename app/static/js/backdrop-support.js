/**
 * Check if backdrop-filter is supported
 * Apply fallbacks if not supported
 */
document.addEventListener('DOMContentLoaded', function() {
    // Check for backdrop-filter support
    const isBackdropFilterSupported = CSS.supports('backdrop-filter', 'blur(12px)') || 
                                     CSS.supports('-webkit-backdrop-filter', 'blur(12px)');
    
    if (!isBackdropFilterSupported) {
        // Apply fallback styles for glass elements
        const glassElements = document.querySelectorAll('.glass');
        
        glassElements.forEach(el => {
            // Increase background opacity for better readability without blur
            el.style.backgroundColor = 'rgba(30, 30, 35, 0.85)';
            el.style.borderColor = 'rgba(255, 255, 255, 0.2)';
            
            // Add a subtle gradient for depth
            el.style.background = 'linear-gradient(to bottom, rgba(40, 40, 45, 0.85), rgba(25, 25, 30, 0.85))';
        });
        
        // Add a class to body for other CSS fallbacks if needed
        document.body.classList.add('no-backdrop-filter');
    }
    
    // Add subtle parallax effect to background
    if (window.innerWidth > 768) { // Only on larger screens
        document.addEventListener('mousemove', function(e) {
            const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
            const moveY = (e.clientY - window.innerHeight / 2) * 0.01;
            
            document.body.style.backgroundPosition = `${moveX}px ${moveY}px`;
        });
    }
}); 