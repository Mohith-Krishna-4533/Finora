document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Counter animation for hero stats
    const counters = document.querySelectorAll('.stat-number');
    
    const animateCounter = (counter) => {
        const target = counter.textContent;
        const isPercentage = target.includes('%');
        const isPlus = target.includes('+');
        const numericValue = parseFloat(target.replace(/[^\d.]/g, ''));
        
        let current = 0;
        const increment = numericValue / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= numericValue) {
                current = numericValue;
                clearInterval(timer);
            }
            
            let displayValue = Math.floor(current);
            if (target.includes('.')) {
                displayValue = current.toFixed(1);
            }
            
            counter.textContent = displayValue + (isPercentage ? '%' : '') + (isPlus ? '+' : '');
        }, 20);
    };

    // Trigger counter animation when hero section is visible
    const heroObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                counters.forEach(counter => {
                    animateCounter(counter);
                });
                heroObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const heroStats = document.querySelector('.hero-stats');
    if (heroStats) {
        heroObserver.observe(heroStats);
    }

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards and sections for animation
    const animatedElements = document.querySelectorAll('.feature-card, .review-card, .pricing-card, .service-item, .step, .bonus-feature, .dashboard-feature');

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });

    // Stats counter animation
    const statsCounters = document.querySelectorAll('.stats-section .stat-number');

    const animateStatsCounter = (counter) => {
        const target = parseFloat(counter.dataset.target);
        const suffix = counter.dataset.suffix || '';
        
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            let displayValue = Math.floor(current);
            if (target % 1 !== 0) {
                displayValue = current.toFixed(1);
            }
            
            counter.textContent = displayValue + suffix;
        }, 30);
    };

    // Trigger stats animation when section is visible
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                statsCounters.forEach(counter => {
                    animateStatsCounter(counter);
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }

    // Dashboard mockup chart animation
    const chartBars = document.querySelectorAll('.bar');
    chartBars.forEach((bar, index) => {
        bar.style.animationDelay = `${index * 0.1}s`;
    });

    // Pricing card hover effects
    const pricingCards = document.querySelectorAll('.pricing-card');

    pricingCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Bonus feature hover effects
    const bonusFeatures = document.querySelectorAll('.bonus-feature');

    bonusFeatures.forEach(feature => {
        feature.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.bonus-icon');
            icon.style.transform = 'scale(1.1) rotate(5deg)';
        });
        
        feature.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.bonus-icon');
            icon.style.transform = 'scale(1) rotate(0deg)';
        });
    });

    // Review cards carousel effect (auto-scroll on larger screens)
    const reviewsGrid = document.querySelector('.reviews-grid');
    if (reviewsGrid && window.innerWidth > 1024) {
        let scrollAmount = 0;
        const scrollStep = 1;
        const scrollDelay = 50;
        
        setInterval(() => {
            if (reviewsGrid.scrollLeft >= (reviewsGrid.scrollWidth - reviewsGrid.clientWidth)) {
                reviewsGrid.scrollLeft = 0;
            } else {
                reviewsGrid.scrollLeft += scrollStep;
            }
        }, scrollDelay);
    }

    // Parallax effect for dashboard mockup
    const dashboardMockup = document.querySelector('.dashboard-mockup');
    if (dashboardMockup) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.2;
            dashboardMockup.style.transform = `translateY(${rate}px)`;
        });
    }

    console.log('Enhanced Finora home page initialized successfully!');
});
