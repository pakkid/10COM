const header = document.querySelector('header');
let lastScrollTop = 0;
let isScrollingToSection = false;

// Function to handle scroll
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    // Skip hiding if scrolling to a section
    if (isScrollingToSection) return;

    // Only hide the header if scrolling down with the mouse
    if (currentScroll > lastScrollTop && currentScroll > header.clientHeight) {
        // Scrolling down
        header.style.transform = 'translateY(-100%)'; // Move header out of view
    } else if (currentScroll < lastScrollTop) {
        // Scrolling up
        header.style.transform = 'translateY(0)'; // Move header back into view
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // For mobile or negative scrolling
});

// Prevent hiding header when clicking nav links
document.querySelectorAll('nav ul li a').forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default anchor behavior

        // Always show the header when clicking nav links
        header.style.transform = 'translateY(0)';
        isScrollingToSection = true;

        // Get the target section ID from the link
        const targetSection = document.querySelector(event.target.getAttribute('href'));

        // Scroll to the target section
        targetSection.scrollIntoView({ behavior: 'smooth' });

        // Reset scrolling behavior
        setTimeout(() => {
            isScrollingToSection = false;
        }, 500); // Adjust this timeout if needed
    });
});

// Reset header hiding on scroll after clicking
window.addEventListener('wheel', () => {
    // Allow header to hide again after clicking a nav link
    isScrollingToSection = false;
});
