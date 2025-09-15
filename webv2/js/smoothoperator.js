const body = document.body;
const main = document.getElementById('main');
const footer = document.getElementById('footer1');

let sx = 0, sy = 0;
let dx = 0, dy = 0;

body.style.height = main.scrollHeight + 'px'; // includes footer height

main.style.position = 'fixed';
main.style.top = 0;
main.style.left = 0;

// Remove fixed positioning from footer!
// footer.style.position = 'fixed';
// footer.style.top = 100;
// footer.style.left = 0;

window.addEventListener('scroll', easeScroll);

function easeScroll() {
    sx = window.pageXOffset;
    sy = window.pageYOffset;
}

window.requestAnimationFrame(render);

function render() {
    dx = li(dx, sx, 0.04);
    dy = li(dy, sy, 0.04);

    dx = Math.floor(dx * 100) / 100;
    dy = Math.floor(dy * 100) / 100;

    main.style.transform = `translate3d(-${dx}px, -${dy}px, 0px)`;

    // Remove footer transform — footer moves inside main
    // footer.style.transform = ...

    window.requestAnimationFrame(render);
}

function li(a, b, n) {
    return (1 - n) * a + n * b;
}
