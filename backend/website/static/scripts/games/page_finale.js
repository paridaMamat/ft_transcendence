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
			setTimeout(() => { // Rediriger vers la page du jeu après 3 secondes
				if (data.type === 'Matchmaking') {
					$('#score1').text(data.score1);
					$('#player2-username').text(data.player2.username);
					$('#score2').text(data.score2);
					localStorage.removeItem('partyId');
					window.location.href = '#accueil';
				} else if (data.type === 'Tournament')
					if (data.tour.current_round !== data.tour.nb_rounds && winner === data.player1)
						window.location.href = '#lobby_partie/?id=' + data.tour.game_id;
					else
						window.location.href = '#accueil';
			}, 3000);
		})

});