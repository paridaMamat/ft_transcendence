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

        console.log(`Finding opponent for game ID: ${gameId}`);

        fetch('/tournament_lobby/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
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
                $('.lobby-opponent-avatar1 img').attr('src', response.opponent.avatar);
                $('#opponent-username1').text(response.opponent.username);
                $('.waiting-indicator').hide();

                // Stocker l'ID de la partie principale pour une utilisation ultérieure
                const party1Id = response.party1.id;
                console.log(`ID de la première partie: ${party1Id}`);

                // Afficher les informations de la deuxième partie
                const opponent1Data = response.match_opponent_1;
                const opponent2Data = response.match_opponent_2;
                $('#opponent-username2').text(opponent1Data.username);
                $('#opponent-username3').text(opponent2Data.username);
                $('.lobby-opponent-avatar2 img').attr('src', opponent1Data.avatar);
                $('.lobby-opponent-avatar3 img').attr('src', opponent2Data.avatar);

                setTimeout(() => {
                    if (gameId === '2') {
                        window.location.href = `#pong3D`;
                    } else if (gameId === '3') {
                        window.location.href = `#memory_game`;
                    } else {
                        console.error('Unknown game ID');
                    }
                }, 8000);
            } else if (response.status === 'waiting') {
                console.log('response.status === waiting');
                setTimeout(findOpponent, 5000);
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
