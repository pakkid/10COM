function scrollSection(sectionNumber) {
    const targetSection = document.getElementById(`section${sectionNumber}`);
    if (targetSection) {
        window.scrollTo({
            top: targetSection.offsetTop - 80, // Adjust for header height
            behavior: 'smooth' // Smooth scroll
        });
    }
}

function teenPage() {
    window.location.href = "./teen/"
}