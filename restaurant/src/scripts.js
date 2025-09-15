const DISCORD_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1404956335820247151/2XaeuoqHCZ6tR-ueMR9sFJQKI5983jwIkBmaGlJvGZ8dP2z1ozDRmqnRckHGRZ4Jalqu';
const GOOGLE_SHEET_WEBAPP_URL = 'https://script.google.com/macros/s/AKfycbxKacrmVjPuThe1AWk_CTlcOm7zcGmavhElTf5XsaiyNUVe97TH4uXXHLsmbhPxw2BjQw/exec';

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('#contact form');
    const submitBtn = document.getElementById('submitBtn');
    
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        if (!validateForm()) return;

        // Start loading state
        setButtonLoading(true);

        const firstName = document.getElementById('firstName').value.trim();
        const lastName = document.getElementById('lastName').value.trim();
        const email = document.getElementById('email').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const subject = document.getElementById('subject').value;
        const message = document.getElementById('message').value.trim();
        const newsletter = document.getElementById('newsletter').checked;

        // Data for Google Sheets
        const formData = { firstName, lastName, email, phone, subject, message, newsletter };

        // Discord message
        const discordMessage = {
            embeds: [{
                title: "New Contact Form Submission - La Ratatouille",
                color: 0x007bff,
                fields: [
                    { name: "Name", value: `${firstName} ${lastName}`, inline: true },
                    { name: "Email", value: `[${email}](mailto:${email})`, inline: true },
                    { name: "Phone", value: phone ? `[${phone}](tel:${phone})` : "N/A", inline: true },
                    { name: "Subject", value: subject, inline: true },
                    { name: "Newsletter", value: newsletter ? "Yes" : "No", inline: true },
                    { name: "Message", value: message, inline: false }
                ],
                timestamp: new Date().toISOString(),
                url: "https://docs.google.com/spreadsheets/d/1e9xyoRQNDoZzNvEwH1ycWDJUDEz3_CykzLgFgd5iZP4/edit?gid=0#gid=0"
            }]
        };

        try {

            console.log(formData)
            
            // 1. Send to Google Sheets
            const sheetResponse = await fetch(GOOGLE_SHEET_WEBAPP_URL, {
                method: 'POST',
                mode: 'no-cors',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            // 2. Send to Discord
            const discordResponse = await fetch(DISCORD_WEBHOOK_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(discordMessage)
            });

            if (discordResponse.ok) {
                showAlert('success', 'Thank you! Your message has been sent successfully.');
                contactForm.reset();
            } else {
                throw new Error('Failed to send Discord message');
            }

        } catch (error) {
            console.error('Error:', error);
            showAlert('danger', 'Sorry, there was an error sending your message.');
        } finally {
            // End loading state
            setButtonLoading(false);
        }
    });

    function setButtonLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.classList.add('btn-loading');
        } else {
            submitBtn.disabled = false;
            submitBtn.classList.remove('btn-loading');
        }
    }

    initSectionScrollHighlight();
});

// --- Section scroll offset + nav highlight ---
function initSectionScrollHighlight() {
    const nav = document.querySelector('.navbar');
    const links = Array.from(document.querySelectorAll('.navbar a.nav-link[href^="#"]'))
        .filter(a => document.querySelector(a.getAttribute('href')));
    const sections = links.map(a => document.querySelector(a.getAttribute('href')));

    function setNavHeightVar() {
        const h = nav.offsetHeight;
        document.documentElement.style.setProperty('--nav-height', h + 'px');
        // update scroll-margin-top dynamically
        sections.forEach(sec => sec.style.scrollMarginTop = h + 'px');
    }
    setNavHeightVar();
    window.addEventListener('resize', debounce(setNavHeightVar, 150));

    // Smooth scroll with precise offset (overrides native to avoid jitter)
    links.forEach(link => {
        link.addEventListener('click', e => {
            const targetId = link.getAttribute('href');
            if (!targetId.startsWith('#')) return;
            e.preventDefault();
            const target = document.querySelector(targetId);
            if (!target) return;
            const y = target.getBoundingClientRect().top + window.scrollY - nav.offsetHeight + 1;
            window.scrollTo({ top: y, behavior: 'smooth' });
        });
    });

    function onScroll() {
        const scrollPos = window.scrollY + nav.offsetHeight + 5;
        let currentIndex = 0;
        sections.forEach((sec, i) => {
            if (sec.offsetTop <= scrollPos) currentIndex = i;
        });
        links.forEach(l => l.classList.remove('active'));
        if (links[currentIndex]) links[currentIndex].classList.add('active');
    }
    document.addEventListener('scroll', throttle(onScroll, 100), { passive: true });
    onScroll();
}

// Simple throttle & debounce utilities (lightweight)
function throttle(fn, wait) {
    let last = 0, t;
    return (...args) => {
        const now = Date.now();
        if (now - last >= wait) {
            last = now;
            fn.apply(this, args);
        } else {
            clearTimeout(t);
            t = setTimeout(() => { last = Date.now(); fn.apply(this, args); }, wait - (now - last));
        }
    };
}
function debounce(fn, wait) {
    let t;
    return (...args) => {
        clearTimeout(t);
        t = setTimeout(() => fn.apply(this, args), wait);
    };
}

function validateForm() {
    const firstName = document.getElementById('firstName').value.trim();
    const email = document.getElementById('email').value.trim();
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value.trim();
    
    let isValid = true;
    let errorMessage = '';
    
    document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    
    if (!firstName) {
        document.getElementById('firstName').classList.add('is-invalid');
        errorMessage += 'First name is required.\n';
        isValid = false;
    }
    
    if (!email) {
        document.getElementById('email').classList.add('is-invalid');
        errorMessage += 'Email is required.\n';
        isValid = false;
    } else if (!isValidEmail(email)) {
        document.getElementById('email').classList.add('is-invalid');
        errorMessage += 'Please enter a valid email address.\n';
        isValid = false;
    }
    
    if (!subject) {
        document.getElementById('subject').classList.add('is-invalid');
        errorMessage += 'Please select a subject.\n';
        isValid = false;
    }
    
    if (!message) {
        document.getElementById('message').classList.add('is-invalid');
        errorMessage += 'Message is required.\n';
        isValid = false;
    } else if (message.length < 10) {
        document.getElementById('message').classList.add('is-invalid');
        errorMessage += 'Message must be at least 10 characters long.\n';
        isValid = false;
    }
    
    if (!isValid) {
        showAlert('danger', 'Please fix the following errors:<br>' + errorMessage.replace(/\n/g, '<br>'));
    }
    
    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showAlert(type, message) {
    document.querySelectorAll('.alert').forEach(alert => alert.remove());
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const form = document.querySelector('#contact form');
    form.parentNode.insertBefore(alertDiv, form);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, type === 'danger' ? 7000 : 5000);
}