async function generer() {
    const cours = document.getElementById("cours").value;
    const resultat = document.getElementById("resultat");

    if (!cours.trim()) {
        resultat.textContent = "❌ Colle un cours d'abord";
        return;
    }

    resultat.textContent = "⏳ Génération en cours...";

    try {
        const response = await fetch("http://localhost:5000/fiche", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cours })
        });

        const data = await response.json();
        resultat.textContent = data.fiche || data.error;

    } catch {
        resultat.textContent = "❌ Serveur non lancé";
    }
}
