
console.log('base.js loaded');

let isLoading = false;
        
function loadContent() {
console.log(isLoading);
// Empêcher le chargement multiple
if (isLoading) return; // Ne pas exécuter si une action de navigation est déjà en cours
isLoading = true;

// Supprimer l'écouteur d'événement hashchange
window.removeEventListener('hashchange', loadContent);


// Mettre à jour l'URL sans recharger la page
history.replaceState({}, '', location.hash);

// Supprimez l'élément <canvas> avant de charger une nouvelle page
var canvasElement = document.querySelector('canvas');
if (canvasElement) {
    canvasElement.remove();
}

// Récupérer le hash de l'URL
    var hash = location.hash;
    console.log(location.hash);
    var content = document.getElementById('content');
    var url = '';

    switch(hash) {
        case '#index':
            url = 'index/';
            break;
        case '#login':
            url = 'login/';
            break;
        case "#games":
            url = "games/";
            break;
        case '#AI':
            url = 'AI/';
            break;
        case '#pong3D':
            url = 'pong3D/';
            break;
        case '#register':
            url = 'register/';
            break;
        case "#memory_game":
            url = "memory_game/";
            break;
        case "#account_settings":
            url = "account_settings/";
            break;
        case "#friends":
            url = "friends/";
            break;
        case "#accueil":
            url = "accueil/";
            break;
        case "#about_us":
            url = "about_us/";
            break;
        default:
            url = "error_404/";
    }

    // Utiliser AJAX pour récupérer le contenu
    var xhr = new XMLHttpRequest();
    console.log(" essai pour log URL " + url);
    xhr.open('GET', url, true);
    xhr.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            // Insérer le contenu récupéré dans l'élément 'content'
            content.innerHTML = "";
            content.innerHTML = this.responseText;
            

             // Supprimer le script chargé pour la page précédente
            var oldScript = document.querySelector('script');
            if (oldScript) {
                oldScript.remove();
            }
            
            // Créer une nouvelle balise <script>
            var script = document.createElement('script');
            // // Modifier la source du script
            // script.setAttribute('src', '{% static 'scripts/index.js' %}');

            // Load the appropriate script based on the URL hash
            switch(hash) {
                case '#index':
                    console.log("Loading index.js");
                    script.src = "{% static 'scripts/index.js' %}";
                    break;
                case '#login':
                    console.log("Loading login.js");
                    script.src = "{% static 'scripts/login.js' %}";
                    break;
                case '#AI':
                    console.log("Loading AI.js");
                    script.src = "{% static 'scripts/three.min.js' %}";                            
                    break;
                case '#friends':
                    console.log("Loading accueil.js");
                    script.src = "{% static 'scripts/friends.js' %}";                          
                    break;
                case '#pong3D':
                    console.log("Loading pong3D.js");
                    script.src = "{% static 'scripts/pong3D.js' %}";
                    break;
                case '#accueil':
                    console.log("Loading accueil.js"); 
                    script.src = "{% static 'scripts/accueil.js' %}";
                    break;
                case '#register':
                    console.log("Loading register.js");
                    script.src = "{% static 'scripts/register.js' %}";
                    break;
                case "#memory_game":
                    console.log("Loading memory_game.js");
                    script.src = "{% static 'scripts/memory_game.js' %}";
                    break;
                case "#account_settings":
                    console.log("Loading account_settings.js");
                    script.src = "{% static 'scripts/account_settings.js' %}";
                    break;
                default:
                    console.log("no script to load");
            }

// Ajouter le script à la page après un court délai
setTimeout(function() {
    document.head.appendChild(script);
}, 500); // 500 est le délai en millisecondes

// Réinitialiser l'écouteur d'événement hashchange
window.addEventListener('hashchange', loadContent);
isLoading = false;


}

else {
// Gérer les erreurs
content.innerHTML = 'Erreur 404: page introuvable';
isLoading = false;
}
};
    xhr.onerror = function() {
        // Gérer les erreurs de réseau
        content.innerHTML = 'Erreur de réseau.';
        //isLoading = false;
    };
    xhr.send();

}

// Écouter l'événement hashchange
window.addEventListener('hashchange', loadContent);

// Écouter l'événement popstate pour gérer le retour et le précédent
window.addEventListener('popstate', loadContent);


// Charger le contenu au chargement initial de la page
document.addEventListener('DOMContentLoaded', loadContent);