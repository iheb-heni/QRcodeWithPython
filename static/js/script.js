// static/js/script.js

document.addEventListener('DOMContentLoaded', (event) => {
    const urlsInput = document.getElementById('urls');
    const generateButton = document.querySelector('button[type="submit"]');

    // Vérification si l'utilisateur a entré une URL
    generateButton.addEventListener('click', (event) => {
        if (!urlsInput.value.trim()) {
            alert('Please enter at least one URL.');
            event.preventDefault();
        }
    });

    // Fonction pour faire disparaître les alertes après 4 secondes
    const alert = document.querySelector('.alert');
    if (alert) {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500); // Correspond au temps de la transition
        }, 4000);
    }
});
