// Add interactivity or form validation here
document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Example validation
    if (username === "admin" && password === "password") {
        alert("Login successful!");
        
    } else {
        alert("Invalid username or password");
    }
});