/* =============================================
   FARMPLACE - Main JavaScript
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {

    // =============================================
    // Navbar Scroll Effect
    // =============================================
    const nav = document.getElementById('mainNav');
    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }

    // =============================================
    // Scroll Reveal Animation
    // =============================================
    const revealElements = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));

    // =============================================
    // Counter Animation
    // =============================================
    const counters = document.querySelectorAll('.counter');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => counterObserver.observe(counter));

    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-target'));
        const suffix = element.getAttribute('data-suffix') || '';
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString() + suffix;
        }, 16);
    }

    // =============================================
    // Typewriter Effect
    // =============================================
    const typewriter = document.querySelector('.typewriter');
    if (typewriter) {
        const phrases = JSON.parse(typewriter.getAttribute('data-phrases') || '[]');
        if (phrases.length > 0) {
            let phraseIndex = 0;
            let charIndex = 0;
            let isDeleting = false;
            let typeSpeed = 100;

            function type() {
                const currentPhrase = phrases[phraseIndex];

                if (isDeleting) {
                    typewriter.textContent = currentPhrase.substring(0, charIndex - 1);
                    charIndex--;
                    typeSpeed = 50;
                } else {
                    typewriter.textContent = currentPhrase.substring(0, charIndex + 1);
                    charIndex++;
                    typeSpeed = 100;
                }

                if (!isDeleting && charIndex === currentPhrase.length) {
                    typeSpeed = 2000;
                    isDeleting = true;
                } else if (isDeleting && charIndex === 0) {
                    isDeleting = false;
                    phraseIndex = (phraseIndex + 1) % phrases.length;
                    typeSpeed = 500;
                }

                setTimeout(type, typeSpeed);
            }

            type();
        }
    }

    // =============================================
    // Smooth Scroll
    // =============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // =============================================
    // Auto-dismiss Alerts
    // =============================================
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // =============================================
    // Payment Status Polling
    // =============================================
    const paymentStatusEl = document.querySelector('[data-payment-id]');
    if (paymentStatusEl) {
        const paymentId = paymentStatusEl.getAttribute('data-payment-id');
        const statusInterval = setInterval(async () => {
            try {
                const response = await fetch(`/api/payments/${paymentId}/status/`);
                const data = await response.json();
                if (data.status === 'completed' || data.status === 'failed') {
                    clearInterval(statusInterval);
                    window.location.reload();
                }
            } catch (e) {
                // ignore polling errors
            }
        }, 3000);
    }

    // =============================================
    // Dark Mode Toggle
    // =============================================
    const themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-bs-theme', savedTheme);

        themeToggle.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-bs-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-bs-theme', next);
            localStorage.setItem('theme', next);
        });
    }

    // =============================================
    // Quantity Controls (Chicks Order)
    // =============================================
    const qtyInput = document.querySelector('#id_quantity');
    if (qtyInput) {
        const max = parseInt(qtyInput.getAttribute('max')) || 9999;
        qtyInput.addEventListener('change', () => {
            let val = parseInt(qtyInput.value) || 1;
            if (val < 1) val = 1;
            if (val > max) val = max;
            qtyInput.value = val;
        });
    }

});
