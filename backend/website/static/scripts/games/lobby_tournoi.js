console.log('Script lobby_tournoi.js is loaded');

$(document).ready(function() {
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    function getGameIdFromUrl() {
        const hash = window.location.hash;
        console.log(`Hash: ${hash}`);
        if (!hash.includes('?')) {
            return null;
        } else {
            const hashParams = new URLSearchParams(hash.substring(hash.indexOf('?')));
            return hashParams.get('id');
        }
    }

    function findOpponent() {
        const csrfToken = getCSRFToken();
        const gameId = getGameIdFromUrl();
        console.log(`CSRF token: ${csrfToken}`);
        console.log(`Game ID: ${gameId}`);

        if (!csrfToken) {
            console.error('CSRF token is missing');
            return;
        }

        if (!gameId) {
            console.error('Game ID is missing');
            return;
        }

        let attemptCount = 0;

        console.log(`Finding opponent for game ID: ${gameId}`);
        const tourId = localStorage.getItem('tourId');
        console.log(`Tournament ID: ${tourId}`);
        fetch(`/tournament_lobby/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
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
                console.log(response);
                // ajouter l'avatar
                $('#current_user').text(response.current_user.alias);
                $('#opponent-username1').text(response.opponent.username);
                $('.waiting-indicator').hide();

                // Stocker l'ID de la partie principale pour une utilisation ultérieure
                const party1Id = response.party1.id;
                console.log(`ID de la première partie: ${party1Id}`);
                localStorage.setItem('partyId', party1Id);
                // Afficher les informations de la deuxième partie
                const opponent1Data = response.match_opponent_1;
                const opponent2Data = response.match_opponent_2;
                $('#opponent-username2').text(opponent1Data.username);
                $('#opponent-username3').text(opponent2Data.username);
                //ajouter l'avatar des 2 autres joueurs

                setTimeout(() => {
                    if (gameId === '2') {
                        window.location.href = `#pong3D`;
                    } else if (gameId === '3') {
                        window.location.href = `#memory_game`;
                    } else {
                        console.error('Unknown game ID');
                    }
                }, 2000);
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
        setTimeout(findOpponent, 2000);
    }

    initialDelay();
});
