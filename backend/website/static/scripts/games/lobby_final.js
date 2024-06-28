console.log('lobby_final.js loaded'); // Log pour confirmer le chargement du script

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
        const tourId = localStorage.getItem('tourId');
        console.log(`CSRF token: ${csrfToken}`); // Log to confirm CSRF token
        console.log(`Game ID: ${gameId}`); // Log to confirm game ID
        console.log(`Tour ID: ${tourId}`); // Log to confirm tour ID

        if (!csrfToken) {
            console.error('CSRF token is missing');
            return;
        }

        if (!gameId) {
            console.error('Game ID is missing');
            return;
        }

        console.log(`Finding opponent for game ID: ${gameId}`); // Log to confirm game ID

        fetch('/tournament_lobby/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Ajout du token CSRF
            },
            body: JSON.stringify({
                id: gameId,
                tour_id: tourId
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
                const partyId = response.party.id;
                console.log('Party ID:', partyId);
                localStorage.setItem('partyId', partyId);
                // Afficher les détails de l'adversaire
                console.log('adversaire :', response.opponent.username);
                $('#user-username').text(response.current_user.alias);
                $('#opponent-avatar').attr('src', response.opponent.avatar);
                $('#opponent-username').text(response.opponent.username);
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
                    console.log('Exceeded maximum attempts, you will be redirected to the game page');
                    window.location.href = '#games_page'; // Redirect to "accueil" page
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