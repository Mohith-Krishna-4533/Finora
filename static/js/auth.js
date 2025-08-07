document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    // Login form handler
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('.btn-submit');
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            // Show loading state
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (result.success) {
                    showFlashMessage(result.message, 'success');
                    setTimeout(() => {
                        window.location.href = result.redirect || '/dashboard';
                    }, 1000);
                } else {
                    showFlashMessage(result.message || 'Login failed', 'error');
                }
                
            } catch (error) {
                console.error('Login error:', error);
                showFlashMessage('An error occurred. Please try again.', 'error');
            } finally {
                // Reset loading state
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
            }
        });
    }

    // Signup form handler
    if (signupForm) {
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirmPassword');
        const passwordStrength = document.getElementById('passwordStrength');

        // Password strength checker
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const strength = checkPasswordStrength(password);
            
            passwordStrength.textContent = strength.text;
            passwordStrength.className = `password-strength ${strength.class}`;
        });

        // Password confirmation checker
        confirmPasswordInput.addEventListener('blur', function() {
            const password = passwordInput.value;
            const confirmPassword = this.value;
            
            if (confirmPassword && password !== confirmPassword) {
                showError(this, 'Passwords do not match');
            } else {
                hideError(this);
            }
        });

        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('.btn-submit');
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());
            
            // Show loading state
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
            
            try {
                const response = await fetch('/api/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (result.success) {
                    showFlashMessage(result.message, 'success');
                    setTimeout(() => {
                        window.location.href = result.redirect || '/login';
                    }, 1500);
                } else {
                    showFlashMessage(result.message || 'Signup failed', 'error');
                }
                
            } catch (error) {
                console.error('Signup error:', error);
                showFlashMessage('An error occurred. Please try again.', 'error');
            } finally {
                // Reset loading state
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
            }
        });
    }

    // Form validation enhancement
    const inputs = document.querySelectorAll('input[required]');

    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                showError(this, 'This field is required');
            } else {
                hideError(this);
            }
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                hideError(this);
            }
        });
    });

    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (this.value && !emailRegex.test(this.value)) {
                showError(this, 'Please enter a valid email address');
            }
        });
    });
});

// Password strength checker
function checkPasswordStrength(password) {
    if (password.length === 0) {
        return { text: '', class: '' };
    }

    let score = 0;

    // Length check
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;

    // Character variety checks
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    if (score < 3) {
        return { text: 'Weak password', class: 'weak' };
    } else if (score < 5) {
        return { text: 'Medium strength', class: 'medium' };
    } else {
        return { text: 'Strong password', class: 'strong' };
    }
}
