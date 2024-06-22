

// import { doRequest } from "../utils/fetch.js";

export const createTournamentHandler = () => {
	const handleClick = (event) => {
		if (event.target.matches("#create")) {
			let data = {
				tour_name: document.getElementById("tour_name").value,
				nb_players: parseInt(
					document.getElementById("nb_players").value,
				),
				id_game: parseInt(document.getElementById("game_id").value),
			};
			doRequest.post(`/api/tournament/create`, data, (data) => {
				if (data.status === "ok") {
					window.location.hash =
						"lobby-tournament?id=" + data.id_tournament;
				} else if (data.status === "error") {
					const messageElement = document.getElementById("message");
					if (!messageElement)
						return;
						// return console.error(
						// 	'Element with class "message" not found',
						// );
					messageElement.textContent = data.message;
				}
			});
		}
	};

	document.body.addEventListener("click", handleClick);
	return () => document.body.removeEventListener("click", handleClick);
};

//code imen


    //   // Capture de l'événement submit du formulaire
		// 	document.getElementById("tournoiForm").addEventListener("submit", function(event) {
		// 		event.preventDefault(); // Empêche le comportement par défaut du formulaire

		// 		// Récupération des valeurs des champs
		// 		const nomTournois = document.getElementById("tournoie").value;
		// 		const nbJoueurs = document.getElementById("joueur").value;
		// 		const pseudo = document.getElementById("Pseudo").value;

		// 		// Envoi des données vers le backend Django
		// 		fetch("/url_de_votre_vue_django/", {
		// 				method: "POST",
		// 				headers: {
		// 						"Content-Type": "application/json",
		// 						"X-CSRFToken": getCookie("csrftoken") // Assurez-vous de capturer le cookie CSRF
		// 				},
		// 				body: JSON.stringify({
		// 						nom_tournois: nomTournois,
		// 						nb_joueurs: nbJoueurs,
		// 						pseudo: pseudo
		// 				})
		// 		})
		// 		.then(response => response.json())
		// 		.then(data => {
		// 				// Gestion de la réponse de votre backend (optionnel)
		// 				console.log(data);
		// 		})
		// 		.catch(error => {
		// 				console.error("Erreur:", error);
		// 		});
		// });

		// // Fonction pour récupérer le cookie CSRF
		// function getCookie(name) {
		// 		let cookieValue = null;
		// 		if (document.cookie && document.cookie !== "") {
		// 				const cookies = document.cookie.split(";");
		// 				for (let i = 0; i < cookies.length; i++) {
		// 						const cookie = cookies[i].trim();
		// 						if (cookie.substring(0, name.length + 1) === name + "=") {
		// 								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		// 								break;
		// 						}
		// 				}
		// 		}
		// 		return cookieValue;
		// }