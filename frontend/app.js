async function loadData() {
  const metrics = await fetch("http://localhost:8000/metrics").then(r => r.json());
  const traces = await fetch("http://localhost:8000/traces").then(r => r.json());

  document.getElementById("metrics").textContent =
    JSON.stringify(metrics, null, 2);

  document.getElementById("traces").textContent =
    JSON.stringify(traces, null, 2);
}

loadData();
