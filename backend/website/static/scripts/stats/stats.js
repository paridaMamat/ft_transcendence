console.log('stats.js');

//pour les elements du menu
getMenuInfos();

function setupTabEventListeners() {
    console.log('setup tab');
    updateDashboardDisplay(1);
    document.querySelectorAll('.tab-link').forEach(tab => {
      tab.addEventListener('click', function() {
        document.querySelectorAll('.tab-link').forEach(t => t.classList.remove('active'));
        this.classList.add('active');
  
        const gameId = this.getAttribute('data-tab') === 'tab1' ? 1 : 
            this.getAttribute('data-tab') === 'tab2' ? 2 :
            this.getAttribute('data-tab') === 'tab3' ? 3 : 1;
        updateDashboardDisplay(gameId);
      });
    });
};

setupTabEventListeners();
// Fonction pour obtenir le suffixe ordinal
function getOrdinalSuffix(n) {
    const s = ["ème", "er", "ème", "ème", "ème"];
    const v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
};

//fct pour time
function formatDuration(time_played) {
    if (time_played) {
        const hours = Math.floor(time_played / 3600);
        const minutes = Math.floor((time_played % 3600) / 60);
        const seconds = time_played % 60;
        return `${hours}h ${minutes}m ${seconds}s`;
    }
};

// recuperer le userId pour affichage de l'historique
// async function getCurrentUserId()
// {
//     try {
//         const response = await fetch('api/users/me/');
//         const data = await response.json();
//         return data.id;
//     }
//     catch (error) {
//         console.error("Error fetching my id", error);
//         return {data: null};
//       }
// };

//recupere les users par jeu
async function fetchAllUserByGame(game_id) {
    try {
        console.log('in fetch Users, game id = ', game_id);
        const response = await fetch(`api/user_stats/retrieveTopFive/${game_id}`);
        const data = await response.json();
        console.log('in fetch Users, data = ', data);
        return data;
    }
    catch (error) {
        console.error("Error fetching users", error);
        return null;
      }
};

// pour recuperer les stats du joueur connecte par jeu
async function fetchMyLeaderboard(game_id, user_id) {
    try{
        console.log('in fetch myLeaderload, game id = ', game_id);
        const response = await fetch(`api/user_stats/retrieveMyBoard/${game_id}/${user_id}`);
        const myLeaderboard = await response.json();
        console.log('fetch my leaderboard: ',myLeaderboard);
        if (myLeaderboard.status == 'error')
            return null;
        return myLeaderboard;
      } catch (error) {
        console.error("Error fetching myLeaderboard:", error);
        return null; 
      }
};

// pour recuperer les dernieres parties du joueur connecte, par jeu
async function fetchMyLastParties(game_id, user_id) {
    console.log('game id et user id =', game_id, ' ', user_id);
    try {
        const response = await fetch(`api/party/retrievePartyByGame/${game_id}/${user_id}`);
        const myLastParties = await response.json();
        console.log('my last parties =', myLastParties);
        return myLastParties;
    } catch (error) {
        console.error('Error fetching last parties:', error);
        return null;  // Rethrow the error to handle it outside this function if needed
    }
};

// affiche les stats basiques du user logge, par jeu
async function displayUserBasicStats(myLeaderboard) {
    console.log('my leaderborad in display basc stats', myLeaderboard);
    if (myLeaderboard.length > 0) {
        // console.log('classement =', myLeaderboard[0].level);
        // console.log('my leaderboard score =', myLeaderboard[0].score);
        // console.log('my leaderboard avg time =', myLeaderboard[0].avg_time_per_party);
        // console.log('my leaderboard time played =', myLeaderboard[0].time_played);
        document.getElementById('classement').textContent = myLeaderboard[0].level;
        document.getElementById('partie_jouee').textContent = myLeaderboard[0].played_parties;
        document.getElementById('tournoi_joue').textContent = myLeaderboard[0].played_tour;
        document.getElementById('score').textContent = myLeaderboard[0].score;
        document.getElementById('avg_time').textContent = formatDuration(myLeaderboard[0].avg_time_per_party);
        document.getElementById('total_time').textContent = formatDuration(myLeaderboard[0].time_played);

    } else if (myLeaderboard) {
        document.getElementById('classement').textContent = 'n/c';
        document.getElementById('partie_jouee').textContent = "0";
        document.getElementById('tournoi_joue').textContent = "0";
        document.getElementById('score').textContent = "0";
        document.getElementById('avg_time').textContent = "0";
        document.getElementById('total_time').textContent = "0";
    
    } else {
        console.error("Erreur lors de la récupération des données", error);
    } 
};

// pour afficher les donnees dans les doughnuts, par jeu
async function displayRatios(myLeaderBoard) {
    if (myLeaderBoard) { //myLearBorad.id
        console.log('leaderboard in display ratios:', myLeaderBoard);
        const stats = myLeaderBoard;  // myLeaderBoard[0];
        const wins1 = stats.won_parties; // 
        const losses1 = stats.lost_parties; // 
        const wins2 = stats.won_tour; // 
        const losses2 = stats.lost_tour; // 
        
        document.addEventListener('DOMContentLoaded', function () {
            var ctx1 = document.getElementById('myChart1').getContext('2d');
            var ctx2 = document.getElementById('myChart2').getContext('2d');
        
            // var wins1 = 30; 
            // var losses1 = 20;
        
            // var wins2 = 40; 
            // var losses2 = 25;
            var myChart1 = new Chart(ctx1, {
                type: 'doughnut',
                myLeaderBoard: {
                    labels: ['Wins', 'Losses'],
                    datasets: [{
                    label: '# of Votes',
                    myLeaderBoard: [won_parties, lost_parties],
                    backgroundColor: [
                        'rgba(0, 255, 0, 0.2)', // Vert avec une opacité de 20%
                        'rgba(255, 0, 0, 0.2)' // Rouge avec une opacité de 20%
                    ],
                    borderColor: [
                        'rgba(0, 255, 0, 1)', // Vert
                        'rgba(255, 0, 0, 1)' // Rouge
                    ],
                    borderWidth: 1 // Épaisseur de la bordure
                        }]
                    },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                boxWidth: 20,
                                padding: 10
                            }
                        },
                        tooltip: {
                            enabled: true
                        }
                    },
                    // Ajoutez ces options pour rendre le texte en gras et changer la couleur de la bordure
                    plugins: {
                        tooltip: {
                            enabled: true
                        },
                        legend: {
                            display: true,
                            labels: {
                                font: {
                                    weight: 'bold' // Rendre le texte en gras
                                }
                            }
                        },
                        doughnut: {
                            cutout: '80%', // Changer le diamètre intérieur du cercle
                            borderWidth: 5, // Changer l'épaisseur de la bordure
                            borderColor: '#5e5555' // Changer la couleur de la bordure
                        }
                    }
                    
                }
            });
                
            var myChart2 = new Chart(ctx2, {
                type: 'doughnut',
                myLeaderBoard: {
                        labels: ['Wins', 'Losses'],
                        datasets: [{
                            label: '# of Votes',
                            myLeaderBoard: [won_tour, lost_tour],
                            backgroundColor: [
                                'rgba(0, 255, 0, 0.2)', // Vert avec une opacité de 20%
                                'rgba(255, 0, 0, 0.2)' // Rouge avec une opacité de 20%
                            ],
                            borderColor: [
                                'rgba(0, 255, 0, 1)', // Vert
                                'rgba(255, 0, 0, 1)' // Rouge
                            ],
                            borderWidth: 1 // Épaisseur de la bordure  
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                                labels: {
                                    boxWidth: 20,
                                    padding: 10
                                }
                            },
                            tooltip: {
                                enabled: true
                            }
                        },
                        // Ajoutez ces options pour rendre le texte en gras et changer la couleur de la bordure
                        plugins: {
                            tooltip: {
                                enabled: true
                            },
                            legend: {
                                display: true,
                                labels: {
                                    font: {
                                        weight: 'bold' // Rendre le texte en gras
                                    }
                                }
                            },
                            doughnut: {
                                cutout: '80%', // Changer le diamètre intérieur du cercle
                                borderWidth: 5, // Changer l'épaisseur de la bordure
                                borderColor: '#5e5555' // Changer la couleur de la bordure
                            }
                        }
                    }
            })
        })
    }
};

async function displayLastParties(myLastParties){   // cercle de classement user
    console.log('in display parties : ', myLastParties);
    if (myLastParties){
        const data = myLastParties
        // tableau score temps adversaire gagnant
        for (let i = 0; i < 5; i++) {
            const scoreKey = `score${i}`;
            const timeKey = `time${i}`;
            const adversaryKey = `adversary${i}`;
            const winnerKey = `winner${i}`;
            if (data[i]) {
                $(`#${scoreKey}`).text(data[i].score1);
                console.log('score: ', data[i].score1);
                $(`#${timeKey}`).text(formatDuration(data[i].duration));
                // console.log('player2 username : ', data[i].player2.username);
                if (!data[i].adversary === null)
                    $(`#${adversaryKey}`).text('AI');
                else
                    $(`#${adversaryKey}`).text(data[i].player2.username);
                if (data[i].winner_name === 'Player 1')
                    $(`#${winnerKey}`).text('Oui');
                else
                    $(`#${winnerKey}`).text('Non');
            }
        }
    }
    else {
        console.error("Erreur lors de la récupération de myLastParties ", error);
    }
};

async function displayBestRanking(leaderboardData){
    if (leaderboardData){
        const data = leaderboardData;
    //3 cercle de classement
            $('#1winner').text(data[0].username || 'Non disponible');
            $('#2winner').text(data[1].username || 'Non disponible');
            $('#3winner').text(data[2].username || 'Non disponible');

        // tableau de user classement score-classement nbr partie
        for (let i = 1; i <= 5; i++) {
            const rankKey = `rank${i}`;
            console.log('rank: ', rankKey);
            const idKey = `id${i}`;
            const scoreClassemetKey = `score-classement${i}`;
            const nbrPartyKey = `nbr-partie${i}`;
            let j = i - 1;
            if (data[j]) {
                $(`#${rankKey}`).text(getOrdinalSuffix(data[j].level));
                $(`#${idKey}`).text(data[j].username);
                $(`#${scoreClassemetKey}`).text(data[j].score);
                $(`#${nbrPartyKey}`).text(data[j].played_parties);
            }
        }
    }
    else {
        console.error("Erreur lors de la récupération de leaderboardData: ", error);
    }
};

async function updateDashboardDisplay(gameId) {
    try {
        const myId = await getUserId();
        console.log('myId is ', myId);
        if (!myId)
            throw new Error('Utilisateur non trouvé');

        const allUsers = await fetchAllUserByGame(gameId);
        if (!allUsers)
            throw new Error('allUsers non trouvés');
        await displayBestRanking(allUsers)
    
        const myLeaderboard = await fetchMyLeaderboard(gameId, myId);
        console.log('learderboard in update', myLeaderboard);
        if (!myLeaderboard) 
            throw new Error('myleaderboard non trouvé');
        await displayUserBasicStats(myLeaderboard);
        await displayRatios(myLeaderboard);
    
        const myLastParties = await fetchMyLastParties(gameId, myId);
        console.log('in updateDashboard', myLastParties);
        if (!myLastParties)
            throw new Error('lst parties non trouvées');
        await displayLastParties(myLastParties);
        // await displayRatios(myLeaderboard);
    } catch (error) {
        console.error('error in update dashboard', error);
    }
};

