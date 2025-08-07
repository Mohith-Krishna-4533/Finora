document.addEventListener('DOMContentLoaded', function() {
    // Load user statistics
    loadUserStats();
    
    // Animate stat counters
    animateStatCounters();
    
    // Add click handlers for action cards
    const actionCards = document.querySelectorAll('.action-card');
    actionCards.forEach(card => {
        card.addEventListener('click', function() {
            const title = this.querySelector('h3').textContent;
            showFlashMessage(`${title} feature coming soon!`, 'info');
        });
    });
});

async function loadUserStats() {
    try {
        const response = await fetch('/api/user-stats');
        const result = await response.json();
        
        if (result.success) {
            updateStatCards(result.data);
        }
    } catch (error) {
        console.error('Error loading user stats:', error);
    }
}

function updateStatCards(stats) {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(element => {
        const target = element.dataset.target;
        const suffix = element.dataset.suffix || '';
        
        if (stats[getStatKey(element)]) {
            element.dataset.target = stats[getStatKey(element)];
            element.textContent = stats[getStatKey(element)] + suffix;
        }
    });
}

function getStatKey(element) {
    const card = element.closest('.stat-card');
    const label = card.querySelector('.stat-content p').textContent.toLowerCase();
    
    const keyMap = {
        'total products': 'totalProducts',
        'active optimizations': 'activeOptimizations',
        'revenue increase': 'revenueIncrease',
        'competitors tracked': 'competitorsTracked'
    };
    
    return keyMap[label] || '';
}

function animateStatCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    const animateCounter = (counter) => {
        const target = parseFloat(counter.dataset.target || counter.textContent);
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

    // Trigger counter animation with intersection observer
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target.querySelector('.stat-number');
                if (counter) {
                    animateCounter(counter);
                }
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => observer.observe(card));
}
