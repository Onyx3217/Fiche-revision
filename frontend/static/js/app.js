async function generate(mode) {
  const text = document.getElementById("input").value;

  const res = await fetch(`/generate/${mode}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const data = await res.json();
  document.getElementById("output").innerText = data.result;
}

function logout() {
  window.location.href = "/auth/logout";
}
