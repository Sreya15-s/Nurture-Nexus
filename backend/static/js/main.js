document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission
    
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("re-password").value;
    let passwordError = document.getElementById("passwordError");
    let confirmPasswordError = document.getElementById("confirmPasswordError");

    // Reset errors
    passwordError.textContent = "";
    confirmPasswordError.textContent = "";

    // Validate password length
    if (password.length < 8) {
        passwordError.textContent = "Password must be at least 8 characters.";
        return;
    }

    // Validate confirm password length
    if (confirmPassword.length < 8) {
        confirmPasswordError.textContent = "Confirm Password must be at least 8 characters.";
        return;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        confirmPasswordError.textContent = "Passwords do not match.";
        return;
    }

    // If validation passes, submit form (you can replace this with actual form submission)
    alert("Registration successful!");
    event.target.submit();
});