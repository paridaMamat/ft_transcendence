console.log("page finale chargée")

getMenuInfos();

$(document).ready(function () {

	function getCSRFToken() {
		return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
	}

	//gestion fin de partie

	const csrfToken = getCSRFToken();
	const partyId = localStorage.getItem('partyId');

	console.log(`CSRF token: ${csrfToken}`); // Log to confirm CSRF token
	console.log(`party ID: ${partyId}`); // Log to confirm party ID

	if (!csrfToken) {
		console.error('CSRF token is missing');
		return;
	}

	if (!partyId) {
		console.error('party ID is missing');
		return;
	}

	console.log(`Ending game for party ID: ${partyId}`);

	fetch(`/api/party/${partyId}/`, {
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
		.then(data => {
			$('#score1').text(data.score1);
			$('#score2').text(data.score2);
			if (data.type === 'Tournament') {
				//console.log("tournoi");
				$('#player1-username').text(data.player1.alias);
			} else {
				//console.log("matchmaking");
				$('#player1-username').text(data.player1.username);
			} 
			
			fetch(`/api/party/${partyId}/getPlayerUserInfo/`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': getCSRFToken()
				},
			});
		})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok ' + response.statusText);
			}
			return response.json();
		})
		.then(player2 => {
			console.log("Player 2 info:", player2);
			$('#avatar-user2').attr('src', player2.avatar);
			$('#player2-username').text(player2.username);
			
			setTimeout(() => { // Rediriger vers la page du jeu après 3 secondes

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
									window.location.href = '#accueil';
								}
							})
					}
					else {
						console.log("fin de matchmaking");
						$('#score1').text(data.score1);
						$('#score2').text(data.score2);
						localStorage.removeItem('partyId');
						window.location.href = '#accueil';
					}
				}
				else {

					window.location.href = '#accueil';
				}
			}, 5000);
		})
		.catch(error => {
			console.error('Error fetching party data:', error);
		});
});