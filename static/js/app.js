// State
let charts = {};

const formatCurrency = (val) => {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0
    }).format(val || 0);
};

// Init on DOM ready
document.addEventListener("DOMContentLoaded", () => {
    setupTabs();
    setupFilters();
    setupSqlPlayground();
    loadDashboardData();
    loadOrdersTable();

    document.getElementById("refresh-btn").addEventListener("click", () => {
        loadDashboardData();
    });
});

// Tab navigation
function setupTabs() {
    const buttons = document.querySelectorAll(".tab-btn");
    buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
            buttons.forEach((b) => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach((c) => c.classList.remove("active"));

            btn.classList.add("active");
            const target = document.getElementById(`tab-${btn.dataset.tab}`);
            if (target) target.classList.add("active");
        });
    });
}

// Load filters from API
async function setupFilters() {
    try {
        const res = await fetch("/api/filters");
        const data = await res.json();

        const catSelect = document.getElementById("filter-category");
        data.categories.forEach((cat) => {
            const opt = document.createElement("option");
            opt.value = cat;
            opt.textContent = cat;
            catSelect.appendChild(opt);
        });

        const regSelect = document.getElementById("filter-region");
        data.regions.forEach((reg) => {
            const opt = document.createElement("option");
            opt.value = reg;
            opt.textContent = reg;
            regSelect.appendChild(opt);
        });

        catSelect.addEventListener("change", loadKpis);
        regSelect.addEventListener("change", loadKpis);

        document.getElementById("reset-filters").addEventListener("click", () => {
            catSelect.value = "";
            regSelect.value = "";
            loadKpis();
        });
    } catch (err) {
        console.error("error loading filters", err);
    }
}

// Fetch and display KPI values
async function loadKpis() {
    const cat = document.getElementById("filter-category").value;
    const reg = document.getElementById("filter-region").value;

    const params = new URLSearchParams();
    if (cat) params.append("category", cat);
    if (reg) params.append("region", reg);

    try {
        const res = await fetch(`/api/kpis?${params.toString()}`);
        const data = await res.json();

        document.getElementById("kpi-revenue").textContent = formatCurrency(data.revenue);
        document.getElementById("kpi-profit").textContent = formatCurrency(data.profit);
        document.getElementById("kpi-margin").textContent = `${data.margin}%`;
        document.getElementById("kpi-orders").textContent = Number(data.orders).toLocaleString();
        document.getElementById("kpi-customers").textContent = Number(data.customers).toLocaleString();
        document.getElementById("kpi-aov").textContent = formatCurrency(data.aov);
    } catch (err) {
        console.error("error loading KPIs", err);
    }
}

// Load all charts
async function loadDashboardData() {
    loadKpis();
    loadMonthlyChart();
    loadCategoryChart();
    loadRegionChart();
    loadPaymentChart();
    loadTopProductsChart();
}

async function loadMonthlyChart() {
    const res = await fetch("/api/charts/monthly");
    const data = await res.json();

    const ctx = document.getElementById("monthlyChart").getContext("2d");
    if (charts.monthly) charts.monthly.destroy();

    charts.monthly = new Chart(ctx, {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Revenue",
                    data: data.revenue,
                    borderColor: "#2563eb",
                    backgroundColor: "rgba(37, 99, 235, 0.08)",
                    fill: true,
                    tension: 0.3,
                    borderWidth: 2
                },
                {
                    label: "Profit",
                    data: data.profit,
                    borderColor: "#16a34a",
                    backgroundColor: "rgba(22, 163, 74, 0.08)",
                    fill: true,
                    tension: 0.3,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" }
            },
            scales: {
                y: {
                    ticks: {
                        callback: (val) => "₹" + (val / 1000).toFixed(0) + "k"
                    }
                }
            }
        }
    });
}

async function loadCategoryChart() {
    const res = await fetch("/api/charts/category");
    const data = await res.json();

    const ctx = document.getElementById("categoryChart").getContext("2d");
    if (charts.category) charts.category.destroy();

    charts.category = new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Revenue",
                    data: data.revenue,
                    backgroundColor: "#3b82f6",
                    borderRadius: 4
                },
                {
                    label: "Profit",
                    data: data.profit,
                    backgroundColor: "#10b981",
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    ticks: {
                        callback: (val) => "₹" + (val / 1000).toFixed(0) + "k"
                    }
                }
            }
        }
    });
}

async function loadRegionChart() {
    const res = await fetch("/api/charts/region");
    const data = await res.json();

    const ctx = document.getElementById("regionChart").getContext("2d");
    if (charts.region) charts.region.destroy();

    charts.region = new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Revenue",
                    data: data.revenue,
                    backgroundColor: ["#1e40af", "#047857", "#d97706", "#7c3aed"],
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    ticks: {
                        callback: (val) => "₹" + (val / 1000).toFixed(0) + "k"
                    }
                }
            }
        }
    });
}

async function loadPaymentChart() {
    const res = await fetch("/api/charts/payment");
    const data = await res.json();

    const ctx = document.getElementById("paymentChart").getContext("2d");
    if (charts.payment) charts.payment.destroy();

    charts.payment = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: data.labels,
            datasets: [
                {
                    data: data.revenue,
                    backgroundColor: ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "right" }
            }
        }
    });
}

async function loadTopProductsChart() {
    const res = await fetch("/api/charts/top-products");
    const data = await res.json();

    const ctx = document.getElementById("topProductsChart").getContext("2d");
    if (charts.topProducts) charts.topProducts.destroy();

    charts.topProducts = new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Revenue (₹)",
                    data: data.revenue,
                    backgroundColor: "#2563eb",
                    borderRadius: 4
                }
            ]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: {
                        callback: (val) => "₹" + (val / 1000).toFixed(0) + "k"
                    }
                }
            }
        }
    });
}

// SQL Playground handler
function setupSqlPlayground() {
    const input = document.getElementById("sql-input");
    const btn = document.getElementById("run-sql-btn");
    const status = document.getElementById("sql-status");

    // Presets
    document.querySelectorAll(".sql-preset-bar .btn-pill").forEach((pill) => {
        pill.addEventListener("click", () => {
            input.value = pill.dataset.query;
            runCustomSql();
        });
    });

    btn.addEventListener("click", runCustomSql);

    async function runCustomSql() {
        const query = input.value.trim();
        if (!query) return;

        status.textContent = "Running query...";
        status.style.color = "#64748b";

        try {
            const res = await fetch("/api/sql", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query })
            });

            const data = await res.json();
            if (!res.ok) {
                status.textContent = `Error: ${data.error}`;
                status.style.color = "#ef4444";
                return;
            }

            status.textContent = `Returned ${data.total_returned} rows${data.truncated ? " (showing first 100)" : ""}`;
            status.style.color = "#16a34a";
            renderSqlTable(data.columns, data.rows);
        } catch (err) {
            status.textContent = "Network error";
            status.style.color = "#ef4444";
        }
    }

    // Run the initial query on load
    runCustomSql();
}

function renderSqlTable(columns, rows) {
    const table = document.getElementById("sql-table");
    const thead = table.querySelector("thead");
    const tbody = table.querySelector("tbody");

    thead.innerHTML = "";
    tbody.innerHTML = "";

    const headerRow = document.createElement("tr");
    columns.forEach((col) => {
        const th = document.createElement("th");
        th.textContent = col;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    rows.forEach((row) => {
        const tr = document.createElement("tr");
        row.forEach((cell) => {
            const td = document.createElement("td");
            td.textContent = cell !== null ? cell : "";
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// Load orders table
async function loadOrdersTable() {
    try {
        const res = await fetch("/api/orders?limit=25");
        const data = await res.json();

        document.getElementById("orders-count-label").textContent = `Showing 25 of ${data.total.toLocaleString()} orders`;

        const tbody = document.getElementById("orders-table").querySelector("tbody");
        tbody.innerHTML = "";

        data.orders.forEach((order) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>#${order.order_id}</td>
                <td>${order.order_date}</td>
                <td>${order.customer_name}</td>
                <td>${order.region}</td>
                <td>${order.category}</td>
                <td>${order.product}</td>
                <td>${order.quantity}</td>
                <td>₹${order.unit_price}</td>
                <td>${(order.discount * 100).toFixed(0)}%</td>
                <td>₹${order.revenue.toFixed(2)}</td>
                <td style="color: ${order.profit >= 0 ? '#16a34a' : '#ef4444'}">₹${order.profit.toFixed(2)}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("error loading orders", err);
    }
}
