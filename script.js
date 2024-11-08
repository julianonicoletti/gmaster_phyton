async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert("Por favor, selecione um arquivo primeiro.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error("Erro no upload do arquivo.");
        }

        const data = await response.json();
        document.getElementById('fileContent').textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error("Erro:", error);
        alert("Falha ao ler o arquivo.");
    }
}
