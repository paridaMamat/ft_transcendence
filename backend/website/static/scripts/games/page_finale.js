console.log("page finale chargée")

getMenuInfos();

// async function sendTourWinner(tourId, player)
// {
// 	const csrfToken = getCSRFToken();
//     if (!csrfToken) 
//     	throw new Error('No CSRF token generated');

// 	const response = await fetch (`api/tournament/update/${tourId}/`, {
// 		method: 'PUT',
// 		headers:{
// 			'Content-Type': 'application/json',
//         'X-CSRFToken': csrfToken
//     	},
//     	body: JSON.stringify({ tour_winner: player.id,
// 			status: 'finished'
// 		})
// 	})
// 	if (!response.ok) {
// 		const errorText = await response.text();
// 		throw new Error(`Network response was not ok: ${response.status} ${response.statusText}\n${errorText}`);
// 	}
// };

$(document).ready(function () {
 
	// function sendTourWinner(tourId, player)
	// {
	// 	console.log('in sendWinTour, tourId = ', tourId);
	// 	console.log('in sendWinTour, player = ', player);
	// 	const csrfToken = getCSRFToken();
	// 	if (!csrfToken) 
	// 		throw new Error('No CSRF token generated');

	// 	const response = fetch (`api/tournament/${tourId}/`, {
	// 		method: 'PUT',
	// 		headers:{
	// 			'Content-Type': 'application/json',
	// 		'X-CSRFToken': csrfToken
	// 		},
	// 		body: JSON.stringify({ tour_winner: player.id,
	// 			status: 'finished'
	// 		})
	// 	})
	// 	if (!response.ok) {
	// 		throw new Error(`Network response was not ok`);
	// 	}
	// };
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
			if (data.game !== 1) {
				console.log("le gagnant est:", data.winner_name);
				console.log("le joueur 1 est:", data.player1);
				$('#player1-username').text(data.player1.username);
				$('#player2-username').text(data.player2.username);
				// $('#score1').text(data.score1);
				// $('#score2').text(data.score2);
			}
			else if (data.game === 1) {
				if (!data.winner_name) {
					console.log("le gagnant est: AI");
					console.log("le joueur 2 est:", data.player2);
					$('#player1-username').text(data.player1.username);
					$('#player2-username').text("AI");
				}
				else {
					console.log("le gagnant est:", data.winner_name);
					console.log("le joueur 1 est:", data.player1);
					$('#player1-username').text(data.player1.username);
					$('#player2-username').text("AI");
				}
				$('#score1').text(data.score1);
				$('#score2').text(data.score2);
			}
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
									// sendTourWinner(tourData.id, data.player1);
									fetch (`api/tournament/${tourData.id}/`, {
										method: 'PUT',
										headers:{
											'Content-Type': 'application/json',
										'X-CSRFToken': csrfToken
										},
										body: JSON.stringify({ tour_winner: data.player1.id,
											status: 'finished'
										})
									})
									fetch (`api/party/${partyId}/`, {
										method: 'PUT',
										headers:{
											'Content-Type': 'application/json',
										    'X-CSRFToken': csrfToken
										    },
										body: JSON.stringify({ tour_winner: 'player 1',
										})
									})
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

					window.location.href = '#accueil';
				}
			}, 5000);
		})
		.catch(error => {
			console.error('Error fetching party data:', error);
		});
});






// 					if (data.type === 'Matchmaking') {
// 						console.log("fin de matchmaking");
// 						$('#score1').text(data.score1);
// 						$('#player2-username').text(data.player2.username);
// 						$('#score2').text(data.score2);
// 						localStorage.removeItem('partyId');
// 						window.location.href = '#accueil';
// 					} else if (data.type === 'Tournament') {
// 						console.log("tournoi");
// 						fetch(`/api/party/${partyId}/getTourDataByParty`, {
// 							method: 'GET',
// 							headers: {
// 								'Content-Type': 'application/json',
// 								'X-CSRFToken': csrfToken  // Ajout du token CSRF
// 							},
// 						})
// 							.then(response => {
// 								if (!response.ok) {
// 									throw new Error('Network response was not ok ' + response.statusText);
// 								}
// 								return response.json();
// 							})
// 							.then(tourData => {
// 								console.log("le round en cours:", tourData.current_round);
// 								console.log("le nombre de rounds total:", tourData.nb_rounds);
// 								console.log("le gagnant:", data.winner);
// 								if (tourData.current_round < tourData.nb_rounds && data.winner === data.player1) {
// 									console.log("prochain tour");
// 									window.location.href = '#lobby_partie/?id=' + tourData.id;
// 								} else {
// 									console.log("fin de tournoi");
// 									window.location.href = '#accueil';
// 								}
// 							})
// 							.catch(error => {
// 								console.error('Error fetching tournament data:', error);
// 							});
// 					}
// 				}, 8000);
// 		})
// 		.catch(error => {
// 			console.error('Error fetching party data:', error);
// 		});
// });