console.log('lobby.js loaded'); // Log pour confirmer le chargement du script

getMenuInfos();

$(document).ready(function() {
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    function getGameIdFromUrl() {
        const hash = window.location.hash; // Get the full hash part of the URL
        console.log(`Hash: ${hash}`); // Log to confirm the hash
        if (!hash.includes('?')) {
            return null;
        } else {
        const hashParams = new URLSearchParams(hash.substring(hash.indexOf('?'))); // Extract and parse the query parameters from the hash
        return hashParams.get('id'); // Get the 'id' parameter value
        }
    }
    
    let attemptCount = 0;

    function findOpponent() {

        const csrfToken = getCSRFToken();
        const gameId = getGameIdFromUrl();
        console.log(`CSRF token: ${csrfToken}`); // Log to confirm CSRF token
        console.log(`Game ID: ${gameId}`); // Log to confirm game ID

        if (!csrfToken) {
            console.error('CSRF token is missing');
            return;
        }

        if (!gameId) {
            console.error('Game ID is missing');
            return;
        }


        console.log(`Finding opponent for game ID: ${gameId}`); // Log to confirm game ID

        fetch('/lobby/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Ajout du token CSRF
            },
            body: JSON.stringify({
                id: gameId
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(response => {
            if (response.status === 'matched') {
                console.log('response.status === matched');
                localStorage.setItem('partyId', response.party.id); // Stocker l'ID de la partie principale pour une utilisation ultérieure
                console.log('Response data:', response);
                console.log('Current user avatar:', response.current_user.avatar);
                console.log('Opponent avatar:', response.opponent.avatar);
                // Afficher les détails de l'adversaire
                // var imgElement = document.getElementById('opponent-avatar');
                // if (imgElement) {
                //     imgElement.src = opponent.avatar
                // }
                $('#user-username').text(response.current_user.username);
                $('.lobby-avatar img').attr('src', response.current_user.avatar);
                $('.lobby-opponent-avatar img').attr('src', response.opponent.avatar);
                $('#opponent-username').text(response.opponent.username);

                console.log('Opponent avatar src after setting:', $('.lobby-opponent-avatar img').attr('src'));
                $('.waiting-indicator').hide();  // Masquer l'indicateur d'attente
                setTimeout(() => { // Rediriger vers la page du jeu après 3 secondes
                    if (gameId === '2') {
                        window.location.href = '#pong3D';
                    } else if (gameId === '3') {
                        window.location.href = '#memory_game';
                    } else {
                        console.error('Unknown game ID');
                    }
                }, 3000);
            } else if (response.status === 'waiting') {
                console.log('response.status === waiting');
                attemptCount++;
                if (attemptCount >= 3) { // Check if attempts exceed 3
                    console.log('Exceeded maximum attempts, you will be redirected to the home page');
                    window.location.href = '#accueil'; // Redirect to "accueil" page
                } else {
                    setTimeout(findOpponent, 5000); // Vérifier à nouveau dans 5 secondes
                }
            }
        })
        .catch(error => {
            console.error('Erreur lors de la requête fetch :', error);
        });
    }

    function initialDelay() {
        console.log('Initial delay before starting to find opponent');
        setTimeout(findOpponent, 2000); // Délai initial de 3 secondes avant de commencer la recherche
    }

    initialDelay();
});