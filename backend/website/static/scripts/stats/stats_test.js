// console.log('stats.js');

// getMenuInfos();

// // fct pour classement 
// // Fonction pour obtenir le suffixe ordinal
// function getOrdinalSuffix(n) {
//     const s = ["ème", "er", "ème", "ème", "ème"];
//     const v = n % 100;
//     return n + (s[(v - 20) % 10] || s[v] || s[0]);
// }

// //fct pour time
// async function formatDuration() {
//     const response = await fetch('/api/user_stats/me');
//     const data = await response.json();
//     if (data.time_played) {
//         const hours = Math.floor(time_played / 3600);
//         const minutes = Math.floor((time_played % 3600) / 60);
//         const seconds = time_played % 60;
//         return `${hours}h ${minutes}m ${seconds}s`;
//     } else {
// 		console.error('Error fetching duration:', response.statusText);
// 	}
// };

// async function fetchCurrentUserName() {
//     const response = await fetch('/api/users/me');
//     const data = await response.json();
//     return data.username;
//   }

//   async function fetchLeaderboardData(gameId) {
//     const leaderboardUrl = `/api/getLeaderboard/${gameId}`;
//     const usersUrl = '/api/users/';
  
//     try {
//       const [leaderboardResponse, usersResponse] = await Promise.all([
//         fetch(leaderboardUrl).then(res => res.json()),
//         fetch(usersUrl).then(res => res.json()),
//       ]);
  
//       return {
//         leaderboardData: leaderboardResponse,
//         usersData: usersResponse,
//       };
//     } catch (error) {
//       // console.error("Error fetching data:", error);
//       return { leaderboardData: null, usersData: null };
//     }
//   }
  
//   function processAndAssociateData(leaderboardData) {
//     const leaderboard = leaderboardData.users.map(entry => {
//       const { user, stat } = entry;
//       let ratio = 0;
//       if (stat.won_parties + stat.lost_parties > 0) {
//           ratio = (stat.won_parties / (stat.won_parties + stat.lost_parties)) * 100;
//       }
  
//       return {
//           username: user.username,
//           avatar: user.avatar || defaultAvatarUrl,
//           nbPlayed: stat.played_parties,
//           level: stat.level,
//           ratio: ratio,
//           nb_win: stat.won_parties,
//           nb_lose: stat.lost_parties,
//       };
//     });
// }

// async function getUserBasicStats(leaderboardData) {
//     // const response = await fetch('/api/user_stats/me');
//     // const data = await response.json();
//     console.log('leaderbord = ', leaderboardData);
//     if (leaderboardData) 
//     {
//         // Mettre à jour le contenu du span avec le nom d'utilisateur
//         document.getElementById('classement').textContent = getOrdinalSuffix(leaderboardData.level);
//         document.getElementById('best_score').textContent = leaderboardData.highest_score;
//         document.getElementById('worst_score').textContent = leaderboardData.lowest_score;
//         document.getElementById('avg_time').textContent = leaderboardData.avg_time_per_party;
//         document.getElementById('total_time').textContent = leaderboardData.time_played;
//         document.getElementById('partie-jouee').textContent = leaderboardData.played_parties;
//         document.getElementById('tournoi_joue').textContent = leaderboardData.played_tour;
//       } else if (!leaderboardData) {
//         // Mettre à jour le contenu du span avec le nom d'utilisateur
//         document.getElementById('classement').textContent = "no data";
//         document.getElementById('best_score').textContent = "no data";
//         document.getElementById('worst_score').textContent = "no data";
//         document.getElementById('avg_time').textContent = "no data";
//         document.getElementById('total_time').textContent = "no data";
//         document.getElementById('partie-jouee').textContent = "no data";
//         document.getElementById('tournoi_joue').textContent = "no data";
//         // Vous pouvez ajouter un comportement pour les utilisateurs non authentifiés ici
//       }
//       else {
//             console.error("Erreur lors de la récupération des données: ", error);
//       }
// }

// // async function getOthersStats() {
// //     try {
// //       const response = await fetch('/api/user_stats/me');
// //       const data = await response.json();
  
// //       // Vérifier si l'utilisateur est authentifié
// //       if (data.lenght > 0) {
// //         // Mettre à jour le contenu du span avec le nom d'utilisateur
// //         document.getElementById('classement').textContent = data.level;
// //         document.getElementById('best_score').textContent = data.highest_score;
// //         document.getElementById('worst_score').textContent = data.lowest_score;
// //         document.getElementById('avg_time').textContent = data.avg_time_per_party;
// //       } else {
// //         console.error('User not authenticated in getMenuData');
// //         // Vous pouvez ajouter un comportement pour les utilisateurs non authentifiés ici
// //       }
// //     } catch (error) {
// //       console.error('There was a problem with the fetch operation:', error);
// //     }
// //     getUserBasicStats();
// //   }

// // PARTIES
// async function getPartyStat() {
//     try {
//       const response = await fetch('/api/user_stats/me');
//       const data = await response.json();
        
//       if (data.id) {
//         const stats = data[0];  // 
//         const wins1 = stats.won_parties; // 
//         const losses1 = stats.lost_parties; // 

//         const wins2 = stats.won_tour; // 
//         const losses2 = stats.lost_tour; // 
//         document.addEventListener('DOMContentLoaded', function () {
//             var ctx1 = document.getElementById('myChart1').getContext('2d');
//             var ctx2 = document.getElementById('myChart2').getContext('2d');
        
//             // var wins1 = 30; 
//             // var losses1 = 20;
        
//             // var wins2 = 40; 
//             // var losses2 = 25;
//             var myChart1 = new Chart(ctx1, {
//                 type: 'doughnut',
//                 data: {
//                     labels: ['Wins', 'Losses'],
//                     datasets: [{
//                     label: '# of Votes',
//                     data: [won_parties, lost_parties],
//                     backgroundColor: [
//                         'rgba(0, 255, 0, 0.2)', // Vert avec une opacité de 20%
//                         'rgba(255, 0, 0, 0.2)' // Rouge avec une opacité de 20%
//                     ],
//                     borderColor: [
//                         'rgba(0, 255, 0, 1)', // Vert
//                         'rgba(255, 0, 0, 1)' // Rouge
//                     ],
//                     borderWidth: 1 // Épaisseur de la bordure
//                         }]
//                     },
//                 options: {
//                     responsive: true,
//                     maintainAspectRatio: false,
//                     plugins: {
//                         legend: {
//                             display: true,
//                             position: 'top',
//                             labels: {
//                                 boxWidth: 20,
//                                 padding: 10
//                             }
//                         },
//                         tooltip: {
//                             enabled: true
//                         }
//                     },
//                     // Ajoutez ces options pour rendre le texte en gras et changer la couleur de la bordure
//                     plugins: {
//                         tooltip: {
//                             enabled: true
//                         },
//                         legend: {
//                             display: true,
//                             labels: {
//                                 font: {
//                                     weight: 'bold' // Rendre le texte en gras
//                                 }
//                             }
//                         },
//                         doughnut: {
//                             cutout: '80%', // Changer le diamètre intérieur du cercle
//                             borderWidth: 5, // Changer l'épaisseur de la bordure
//                             borderColor: '#5e5555' // Changer la couleur de la bordure
//                         }
//                     }
                    
//                 }
//             });
                
//             var myChart2 = new Chart(ctx2, {
//                 type: 'doughnut',
//                     data: {
//                         labels: ['Wins', 'Losses'],
//                         datasets: [{
//                             label: '# of Votes',
//                             data: [won_tour, lost_tour],
//                             backgroundColor: [
//                                 'rgba(0, 255, 0, 0.2)', // Vert avec une opacité de 20%
//                                 'rgba(255, 0, 0, 0.2)' // Rouge avec une opacité de 20%
//                             ],
//                             borderColor: [
//                                 'rgba(0, 255, 0, 1)', // Vert
//                                 'rgba(255, 0, 0, 1)' // Rouge
//                             ],
//                             borderWidth: 1 // Épaisseur de la bordure  
//                         }]
//                     },
//                     options: {
//                         responsive: true,
//                         maintainAspectRatio: false,
//                         plugins: {
//                             legend: {
//                                 display: true,
//                                 position: 'top',
//                                 labels: {
//                                     boxWidth: 20,
//                                     padding: 10
//                                 }
//                             },
//                             tooltip: {
//                                 enabled: true
//                             }
//                         },
//                         // Ajoutez ces options pour rendre le texte en gras et changer la couleur de la bordure
//                         plugins: {
//                             tooltip: {
//                                 enabled: true
//                             },
//                             legend: {
//                                 display: true,
//                                 labels: {
//                                     font: {
//                                         weight: 'bold' // Rendre le texte en gras
//                                     }
//                                 }
//                             },
//                             doughnut: {
//                                 cutout: '80%', // Changer le diamètre intérieur du cercle
//                                 borderWidth: 5, // Changer l'épaisseur de la bordure
//                                 borderColor: '#5e5555' // Changer la couleur de la bordure
//                             }
//                         }
//                     }    
//             });
//         });

//          // cercle de classement user
//         $('#classement').text(getOrdinalSuffix(stats.level));
//         //tableux de temp meilleur et pire score 
//         $('#avg_time').text(formatDuration(stats.avg_time_per_party));
//          $('#total_time').text(formatDuration(stats.time_played));
//         $('#best_score').text(stats.highest_score);
//         $('#worst_score').text(stats.lowest_score);
//         //partie et tounoie jouee 
//         $('#parties-jouees').text(stats.played_parties);
//         $('#tournois-joues').text(stats.played_tour);

//         // tableau score temps adversaire gagnant
//         for (let i = 1; i <= 5; i++) {
//             const scoreKey = `score${i}`;
//             const timeKey = `temps${i}`;
//             const adversaryKey = `adversaire${i}`;
//             const winnerKey = `gagnant${i}`;
//             if (stats[scoreKey]) {
//                 $(`#${scoreKey}`).text(stats[scoreKey]);
//                 $(`#${timeKey}`).text(formatDuration(stats[timeKey]));
//                 $(`#${adversaryKey}`).text(stats[adversaryKey]);
//                 $(`#${winnerKey}`).text(stats[winnerKey] ? 'Oui' : 'Non');
//             }
//         }
//     }
//     }
//     catch {
//         {
//             console.error("Erreur lors de la récupération des données: ", error);
//         }
//     }
//     getPartyStat();
// };


// async function getBestRanking(leaderboard){
//     try {
//         const response = await fetch('/api/user_stats/retrieve5first/');
//         const data = await response.json();
//         users = fetchAllUserName();
//         // Vérifier si l'utilisateur est authentifié
//         if (users) {
//     //3 cercle de classement
//             $('#1gagnant').text(leaderboard[0].username || 'Non disponible');
//             $('#2gagnant').text(leaderboard[1].username || 'Non disponible');
//             $('#3gagnant').text(leaderboard[2].username || 'Non disponible');
//         }
//         // tableau de user classement score-classement nbr partie
//         for (let i = 1; i <= 5; i++) {
//             const rankKey = `rank${i}`;
//             const idKey = `id${i}`;
//             const scoreClassemetKey = `score-classement${i}`;
//             const nbrPartyKey = `nbr-partie${i}`;

//             if (data[i]) {
//                 $(`#${rankKey}`).text(getOrdinalSuffix(data[i].level));
//                 $(`#${idKey}`).text(leaderboard[i].username);
//                 $(`#${scoreClassemetKey}`).text(data[i].score);
//                 $(`#${nbrPartyKey}`).text(data[i].played_parties);
//             }
//         }
//     }
//     catch {
//         {
//             console.error("Erreur lors de la récupération des données: ", error);
//         }
//     }
// } 

// // document.addEventListener('DOMContentLoaded', function() {
// //     getBestRanking();
// // });

// // $(document).ready(function(){
// //     getBestRanking();
// // });

// // $(document).ready(function(){
// //     getUserBasicStats();
// // });

// getMenuInfos();

// async function updateDashboardDisplay(gameId) {
//     const { leaderboardData, usersData } = await fetchLeaderboardData(gameId);
//     if (leaderboardData.status === "ok" && usersData.status === "ok") {
//         const leaderboard = processAndAssociateData(leaderboardData);
//         getBestRanking(leaderboard);
//         getUserBasicStats(leaderboard);
//         // displayLeaderboard(leaderboard);
//         // updateDashboardStats(leaderboard);
//         // updateWinLossChart(leaderboard);
//     } else {
//         // console.error("Failed to fetch data");
//     }
//   }

//   export function setupTabEventListeners() {
//     document.querySelectorAll('.tab-link').forEach(tab => {
//       tab.addEventListener('click', function() {
//         document.querySelectorAll('.tab-link').forEach(t => t.classList.remove('active'));
//         this.classList.add('active');
  
//         // const gameId = this.getAttribute('data-tab') === 'tab1' ? 1 : 2;
//         const gameId = 2;
//         updateDashboardDisplay(gameId);
//       });
//     });
//   }