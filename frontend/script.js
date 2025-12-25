async function generer() {
    const cours = document.getElementById("cours").value;
    const resultat = document.getElementById("resultat");
    const btn = document.getElementById("btn");

    if (!cours.trim()) {
        resultat.textContent = "❌ Colle un cours d'abord";
        return;
    }

    // UI chargement
    btn.disabled = true;
    resultat.textContent = "⏳ Génération en cours… (le serveur peut mettre 30s à démarrer)";

    try {
        const response = await fetch("/fiche", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cours })
        });

        const data = await response.json();

        resultat.textContent = data.fiche || "❌ Erreur de génération";

    } catch (error) {
        resultat.textContent = "❌ Serveur indisponible (Render en veille ?)";
    }

    btn.disabled = false;
}
