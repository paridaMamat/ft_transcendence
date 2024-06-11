console.log('stats.js');

// getMenuInfos();

// fct pour classement 
$(document).ready(function(){
    function getOrdinalSuffix(rank) {
        if (rank === 1) {
            return '1er';
        } else if (rank === 2) {
            return '2ème';
        } else if (rank === 3) {
            return '3ème';
        }
    }
});

//fct pour time
async function formatDuration() {
    const response = await fetch('/api/user_stats/me');
    const data = await response.json();
    if (data.time_played) {
        const hours = Math.floor(time_played / 3600);
        const minutes = Math.floor((time_played % 3600) / 60);
        const seconds = time_played % 60;
        return `${hours}h ${minutes}m ${seconds}s`;
    } else {
		console.error('Error fetching duration:', response.statusText);
	}
};

async function getUserBasicStats() {
    try {
      const response = await fetch('/api/user_stats/me');
      const data = await response.json();
  
      // Vérifier si l'utilisateur est authentifié
      if (data.username) {
        // Mettre à jour le contenu du span avec le nom d'utilisateur
        document.getElementById('classement').textContent = data.level;
        document.getElementById('best_score').textContent = data.highest_score;
        document.getElementById('worst_score').textContent = data.lowest_score;
        document.getElementById('avg_time').textContent = data.avg_time_per_party;
        document.getElementById('total_time').textContent = data.time_played;
        document.getElementById('partie-jouee').textContent = data.played_parties;
        document.getElementById('tournoi_joue').textContent = data.played_tour;
      } else {
        console.error('User not authenticated in getMenuData');
        // Vous pouvez ajouter un comportement pour les utilisateurs non authentifiés ici
      }
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  }

  async function getOthersStats() {
    try {
      const response = await fetch('/api/user_stats/retrieve5first/');
      const data = await response.json();
  
      // Vérifier si l'utilisateur est authentifié
      if (data[0]) {
        // Mettre à jour le contenu du span avec le nom d'utilisateur
        document.getElementById('classement').textContent = data.level;
        document.getElementById('best_score').textContent = data.highest_score;
        document.getElementById('worst_score').textContent = data.lowest_score;
        document.getElementById('avg_time').textContent = data.avg_time_per_party;
      } else {
        console.error('User not authenticated in getMenuData');
        // Vous pouvez ajouter un comportement pour les utilisateurs non authentifiés ici
      }
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
    getUserBasicStats();
  }

// PARTIES
async function getPartyStat() {
    try {
      const response = await fetch('/api/user_stats/me');
      const data = await response.json();
        
      if (data.id) {
        const stats = data[0];  // 
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
                data: {
                    labels: ['Wins', 'Losses'],
                    datasets: [{
                    label: '# of Votes',
                    data: [won_parties, lost_parties],
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
                    data: {
                        labels: ['Wins', 'Losses'],
                        datasets: [{
                            label: '# of Votes',
                            data: [won_tour, lost_tour],
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
        });

         // cercle de classement user
        $('#classement').text(getOrdinalSuffix(stats.level));
        //tableux de temp meilleur et pire score 
        $('#avg_time').text(formatDuration(stats.avg_time_per_party));
         $('#total_time').text(formatDuration(stats.time_played));
        $('#best_score').text(stats.highest_score);
        $('#worst_score').text(stats.lowest_score);
        //partie et tounoie jouee 
        $('#parties-jouees').text(stats.played_parties);
        $('#tournois-joues').text(stats.played_tour);

        // tableau score temps adversaire gagnant
        for (let i = 1; i <= 5; i++) {
            const scoreKey = `score${i}`;
            const timeKey = `temps${i}`;
            const adversaryKey = `adversaire${i}`;
            const winnerKey = `gagnant${i}`;
            if (stats[scoreKey]) {
                $(`#${scoreKey}`).text(stats[scoreKey]);
                $(`#${timeKey}`).text(formatDuration(stats[timeKey]));
                $(`#${adversaryKey}`).text(stats[adversaryKey]);
                $(`#${winnerKey}`).text(stats[winnerKey] ? 'Oui' : 'Non');
            }
        }
    }
    }
    catch {
        {
            console.error("Erreur lors de la récupération des données: ", error);
        }
    }
    getPartyStat();
};


async function getBestRanking(){
    try {
        const response = await fetch('/api/user_stats/retrieve5first/');
        const data = await response.json();
    
        // Vérifier si l'utilisateur est authentifié
        if (data[0]) {
    //3 cercle de classement
            $('#1gagnant').text(data[0].username || 'Non disponible');
            $('#2gagnant').text(data[1].username || 'Non disponible');
            $('#3gagnant').text(data[2].username || 'Non disponible');
        }
        // tableau de user classement score-classement nbr partie
        for (let i = 1; i <= 5; i++) {
            const idKey = `id${i}`;
            const rankKey = `classement${i}`;
            const scoreClassemetKey = `score-classemet${i}`;
            const nbrPartyKey = `nbr-partie${i}`;
            if (stats[idKey]) {
                $(`#${idKey}`).text(stats[idKey]);
                $(`#${rankKey}`).text(getOrdinalSuffix(stats[rankKey]));
                $(`#${scoreClassemetKey}`).text(stats[scoreClassemetKey]);
                $(`#${nbrPartyKey}`).text(stats[nbrPartyKey]);
            }
        }
    }
    catch {
        {
            console.error("Erreur lors de la récupération des données: ", error);
        }
    }
    getBestRanking();
};   

getMenuInfos();
// getUserBasicStats();
// getBestRanking();
// getPartyStat() ;
// getOthersStats();