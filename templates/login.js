function handleLogin(event) {
    event.preventDefault();
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    authenticateUser(username, password);
}

function authenticateUser(username, password) {
    // Simulate sending the credentials to the server for validation
    // Replace this with actual server-side authentication logic
    if (username === "demo" && password === "password") {
        alert("Login successful!");
    } else {
        alert("Invalid credentials. Please try again.");
    }
}
