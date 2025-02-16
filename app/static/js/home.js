function validateForm() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const errorMsg = document.getElementById('error-msg');

    if (password.length < 6) {
        errorMsg.textContent = 'Password must be at least 6 characters long.';
        return false;
    }

    if (password !== confirmPassword) {
        errorMsg.textContent = 'Passwords do not match.';
        return false;
    }

    errorMsg.textContent = '';
    return true;
}