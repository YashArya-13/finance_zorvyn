const API = "http://127.0.0.1:8000";

function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(`${API}/users/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        localStorage.setItem("token", data.access_token);
        window.location.href = "dashboard.html";
    });
}
function loadDashboard() {
    const token = localStorage.getItem("token");

    fetch(`${API}/dashboard/summary`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("income").innerText = data.total_income;
        document.getElementById("expense").innerText = data.total_expense;
        document.getElementById("balance").innerText = data.net_balance;

        drawChart(data);
    });
}

function drawChart(data) {
    const ctx = document.getElementById("chart").getContext("2d");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Income", "Expense"],
            datasets: [{
                label: "Finance",
                data: [data.total_income, data.total_expense]
            }]
        }
    });
}

// Auto load
if (window.location.pathname.includes("dashboard.html")) {
    loadDashboard();
}