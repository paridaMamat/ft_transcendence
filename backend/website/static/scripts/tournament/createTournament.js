$(document).ready(function () {
    const tournoiForm = $('#tournoiForm');

    tournoiForm.on('submit', async function (event) {
        event.preventDefault();  // Empêche l'envoi par défaut du formulaire
        console.log("Form submitted");

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const gameId = getGameIdFromUrl();

        if (!csrfToken || !gameId) {
            console.error('CSRF token or Game ID is missing');
            return;
        }

        const nomTournoi = $('#tournoie').val();
        const alias = $('#Pseudo').val();

        if (!nomTournoi || !alias) {
            console.error('Missing form values');
            return;
        }

        try {
            const userData = await getCurrentUser(csrfToken);
            const userId = userData.id;

            const tournamentData = await createTournament(csrfToken, gameId, nomTournoi, userId);
            console.log("Tournament created:", tournamentData);
            localStorage.setItem('tourId', tournamentData.id);

            const updatedUserData = await updateUserAlias(csrfToken, userId, alias);
            console.log("User alias updated:", updatedUserData);
            window.location.href = `#lobby_tournoi?id=${gameId}`;
        } catch (error) {
            console.error('Error:', error);
        }
    });

    async function getCurrentUser(csrfToken) {
        const response = await fetch('/api/users/me/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch current user');
        }

        return await response.json();
    }

    async function createTournament(csrfToken, gameId, nomTournoi, tourCreatorId) {
        const response = await fetch('/api/tournament/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                tour_name: nomTournoi,
                nb_players: 4,
                nb_rounds: 3,
                tour_game: gameId,
                tour_creator: tourCreatorId,
                current_round: 0,
                status: 'waiting',
                remaining_players: 4,
                tour_winner: null,
            })
        });

        if (!response.ok) {
            throw new Error('Failed to create tournament');
        }

        return await response.json();
    }

    async function updateUserAlias(csrfToken, userId, alias) {
        console.log(`Attempting to update alias for user with ID: ${userId}`);
        const response = await fetch(`/api/users/update_alias/${userId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                alias: alias,
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to update user alias');
        }

        return await response.json();
    }

    function getGameIdFromUrl() {
        const hash = window.location.hash;
        return hash.includes('?') ? new URLSearchParams(hash.substring(hash.indexOf('?'))).get('id') : null;
    }
});
