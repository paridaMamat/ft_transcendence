$(document).ready(async function () {
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    const csrfToken = getCSRFToken();
    const partyId = localStorage.getItem('partyId');

    console.log(`CSRF token: ${csrfToken}`);
    console.log(`party ID: ${partyId}`);

    if (!csrfToken) {
        console.error('CSRF token is missing');
        return;
    }

    if (!partyId) {
        console.error('party ID is missing');
        return;
    }

    console.log(`Ending game for party ID: ${partyId}`);

    try {
        const partyResponse = await fetch(`/api/party/${partyId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        });

        if (!partyResponse.ok) {
            throw new Error('Network response was not ok ' + partyResponse.statusText);
        }

        const data = await partyResponse.json();

        // if (data.game === 1) {
        //     if (!data.winner_name) {
        //         console.log("le gagnant est: AI");
        //         console.log("le joueur 2 est:", data.player2);
        //         $('#player1-username').text(data.player1.username);
        //         $('#player2-username').text("AI");
        //     }
        //     else {
        //         console.log("le gagnant est:", data.winner_name);
        //         console.log("le joueur 1 est:", data.player1);
        //         $('#score1').text(data.score1);
        //         $('#score2').text(data.score2);
        //         $('#player1-username').text(data.player1.username);
        //         $('#player2-username').text("AI");
        //     }
        // }
        // else {
        console.log("le gagnant est:", data.winner_name);
        console.log("le joueur 1 est:", data.player1);
        $('#score1').text(data.score1);
        $('#score2').text(data.score2);
        if (data.type === 'Tournament') {
            $('#player1-username').text(data.player1.alias);
        } else {
            $('#player1-username').text(data.player1.username);
        }

        if (data.game === 1) {
            console.log("le joueur 2 est:", data.player2);
            $('#player2-username').text("AI");
        }
        else {
        const player2Response = await fetch(`/api/party/${partyId}/getPlayerUserInfo/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        if (!player2Response.ok) {
            throw new Error('Network response was not ok ' + player2Response.statusText);
        }

        const player2 = await player2Response.json();
        console.log("Player 2 info:", player2);
		$('#avatar-user2').attr('src', player2.avatar);
        $('#player2-username').text(player2.username);
    }

		setTimeout(() => {
			gameId = data.game;
			console.log("gameId:", gameId);

			if (data.winner_name === 'player 1') {

				if (data.type === 'Tournament') {
					console.log("tournoi");
					fetch(`/api/party/${partyId}/getTourDataByParty`, {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json',
							'X-CSRFToken': csrfToken  // Ajout du token CSRF
						},
					})
					.then(response => {
							if (!response.ok) {
								throw new Error('Network response was not ok ' + response.statusText);
							}
							return response.json();
					})
					.then(tourData => {
							console.log("le round en cours:", tourData.current_round);
							console.log("le nombre de rounds total:", tourData.nb_rounds);
							localStorage.removeItem('partyId');
							if (tourData.current_round < tourData.nb_rounds) {
								console.log("prochain tour de jeu");
								window.location.href = `#lobby_final/?id=${gameId}`;
							} else {
								console.log("fin de tournoi, tu as gagné!");
								window.location.href = '#games_page';
							}
						})
				}
				else {
					console.log("fin de matchmaking");
					$('#score1').text(data.score1);
					$('#score2').text(data.score2);
					localStorage.removeItem('partyId');
					window.location.href = '#games_page';
				}
			}
			else {
				window.location.href = '#games_page';
			}
	}, 5000);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
});
