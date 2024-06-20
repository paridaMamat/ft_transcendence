



// import { doRequest } from "../utils/fetch.js";

// export const createTournamentHandler = () => {
// 	const handleClick = (event) => {
// 		if (event.target.matches("#create")) {
// 			let data = {
// 				tour_name: document.getElementById("tour_name").value,
// 				nb_players: parseInt(
// 					document.getElementById("nb_players").value,
// 				),
// 				id_game: parseInt(document.getElementById("game_id").value),
// 			};
// 			doRequest.post(`/api/tournament/create`, data, (data) => {
// 				if (data.status === "ok") {
// 					window.location.hash =
// 						"lobby-tournament?id=" + data.id_tournament;
// 				} else if (data.status === "error") {
// 					const messageElement = document.getElementById("message");
// 					if (!messageElement)
// 						return;
// 						// return console.error(
// 						// 	'Element with class "message" not found',
// 						// );
// 					messageElement.textContent = data.message;
// 				}
// 			});
// 		}
// 	};

// 	document.body.addEventListener("click", handleClick);
// 	return () => document.body.removeEventListener("click", handleClick);
// };

//code imen


// Capture de l'événement submit du formulaire
	document.getElementById("tournoiForm").addEventListener("submit", function(event) {
		event.preventDefault(); // Empêche le comportement par défaut du formulaire

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

		// Récupération des valeurs des champs
		const nomTournoi = document.getElementById("tournoie").value;
		const pseudo = document.getElementById("Pseudo").value;
		

		// Envoi des données vers le backend Django
    // Send the data to the backend
    fetch('api/tournament/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken // Ensure the CSRF token is included
        },
        body: JSON.stringify({
            tour_name: nomTournoi,
            nb_players: 4,
            nb_rounds: 6,
            tour_game: gameId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Tournament created:", data);
        return fetch('api/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                alias: pseudo,
            }),
        });
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(userData => {
        console.log("User created:", userData);
        window.location.href = `lobby-tournament?id=${gameId}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


// 		.then(response => response.json())
// 		.then(data => {
// 			if (data.id) {
// 				console.log("Tournament created with ID:", data.id);
// 				// Store the ID for future updates if necessary
// 				window.location.href = `lobby-tournament?id=${gameId}`;

// 			} else {
// 				console.error("Error creating tournament:", data);
// 			}
// 		})
// 		.catch(error => {
// 				console.error("Erreur:", error);
// 		});
// });
