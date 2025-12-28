async function call(type) {
    const coursEl = document.getElementById("cours");
    const passwordEl = document.getElementById("password");
    const result = document.getElementById("resultat");
    const button = document.querySelector(`button[onclick="call('${type}')"]`);

    if (!passwordEl.value.trim()) {
        result.textContent = "❌ Mot de passe requis";
        return;
    }

    if (!coursEl.value.trim()) {
        result.textContent = "❌ Aucun texte fourni";
        return;
    }

    result.textContent = "⏳ Génération en cours...";
    button.classList.add('loading');
    button.disabled = true;

    try {
        const res = await fetch(`http://localhost:5000/${type}`, {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cours: coursEl.value, password: passwordEl.value })
        });

        const data = await res.json();
        if (data.error) {
            result.textContent = `❌ ${data.error}`;
        } else {
            result.innerHTML = `<span class="success">✅ ${data.result}</span>`;
        }

    } catch (err) {
        result.textContent = "❌ Impossible de contacter le serveur";
        console.error(err);
    } finally {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

async function scan(input) {
    const result = document.getElementById("resultat");
    const fileText = document.getElementById("file-text");

    if (!input.files || !input.files[0]) {
        result.textContent = "❌ Aucune image sélectionnée";
        fileText.textContent = "Choisir une image"; // Reset le texte
        return;
    }

    // Met à jour le texte avec le nom du fichier
    fileText.textContent = input.files[0].name;

    const form = new FormData();
    form.append("image", input.files[0]);

    result.textContent = "📷 Analyse de l’image en cours...";

    try {
        const res = await fetch("http://localhost:5000/scan", {
            method: "POST",
            body: form
        });

        const data = await res.json();

        if (data.cours && data.cours.trim()) {
            document.getElementById("cours").value = data.cours;
            result.innerHTML = `<span class="success">✅ Texte extrait (à corriger si besoin)</span>`;
        } else {
            result.textContent = "⚠️ Aucun texte détecté";
        }

    } catch (err) {
        result.textContent = "❌ Erreur OCR";
        console.error(err);
    }
}