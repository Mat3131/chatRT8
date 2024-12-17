document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username: username, password: password })
    });

    const data = await response.json();
    
    if (data.success) {
        window.location.href = "/main"; // Redirect to main page if login is successful
    } else {
        alert("Username o password errati!");
    }
});
