// Main JavaScript file for Books for All
document.addEventListener('DOMContentLoaded', function() {
    console.log('Books for All JavaScript loaded');
    
    // Dropdown menu functionality
    const dropdowns = document.querySelectorAll('.nav-item.dropdown');
    
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function() {
            this.querySelector('.dropdown-menu').style.opacity = '1';
            this.querySelector('.dropdown-menu').style.visibility = 'visible';
        });
        
        dropdown.addEventListener('mouseleave', function() {
            this.querySelector('.dropdown-menu').style.opacity = '0';
            this.querySelector('.dropdown-menu').style.visibility = 'hidden';
        });
    });
    
    // Back to top button
    const backToTopBtn = document.querySelector('.back-to-top');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});
