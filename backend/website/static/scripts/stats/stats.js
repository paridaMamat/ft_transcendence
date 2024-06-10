console.log('stats.js');

getMenuInfos();

// fct pour classement 
$(document).ready(function(){
    function getOrdinalSuffix(rank) {
        if (rank === 1) {
            return '1er';
        } else if (rank === 2) {
            return '2ème';
        } else if (rank === 3) {
            return '3ème';
        } else {
            return rank + 'ème';
        }
    }
//fct pour time
    function formatDuration(duration) {
        const hours = Math.floor(duration / 3600);
        const minutes = Math.floor((duration % 3600) / 60);
        const seconds = duration % 60;
        return `${hours}h ${minutes}m ${seconds}s`;
    }

    $.ajax({
        url: '/api/tournament/',  
        method: 'GET',
        success: function(data) {
            if (data.length > 0) {
                const tournament = data[0];  // 
                const wins1 = tournament.wins1; // 
                const losses1 = tournament.losses1; // 

                const wins2 = tournament.wins2; // 
                const losses2 = tournament.losses2; // 
                document.addEventListener('DOMContentLoaded', function () {
                    var ctx1 = document.getElementById('myChart1').getContext('2d');
                    var ctx2 = document.getElementById('myChart2').getContext('2d');
                
                    var wins1 = 30; 
                    var losses1 = 20;
                
                    var wins2 = 40; 
                    var losses2 = 25;
                
                    var myChart1 = new Chart(ctx1, {
                        type: 'doughnut',
                        data: {
                            labels: ['Wins', 'Losses'],
                            datasets: [{
                                label: '# of Votes',
                                data: [wins1, losses1],
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
                                data: [wins2, losses2],
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
                $('#classement').text(getOrdinalSuffix(tournament.ranking));
                //tableux de temp meilleur et pire score 
                $('#temp-moyen').text(formatDuration(tournament.average_time));
                $('#temp-total').text(formatDuration(tournament.total_time));
                $('#meilleur-score').text(formatDuration(tournament.best_score));
                $('#pire-score').text(formatDuration(tournament.worst_score));
                //partie et tounoie jouee 
                $('#partie-jouee').text(tournament.games_played);
                $('#tournoie-jouee').text(tournament.tournaments_played);

                // tableau score temps adversaire gagnant
                for (let i = 1; i <= 5; i++) {
                    const scoreKey = `score${i}`;
                    const tempKey = `temp${i}`;
                    const adversaireKey = `adversaire${i}`;
                    const gagnantKey = `gagnant${i}`;
                    if (tournament[scoreKey]) {
                        $(`#${scoreKey}`).text(tournament[scoreKey]);
                        $(`#${tempKey}`).text(formatDuration(tournament[tempKey]));
                        $(`#${adversaireKey}`).text(tournament[adversaireKey]);
                        $(`#${gagnantKey}`).text(tournament[gagnantKey] ? 'Oui' : 'Non');
                    }
                }
                //3 cercle de classement
                $('#1gagnat').text(tournament.gagnant1 || 'Non disponible');
                $('#2gagnat').text(tournament.gagnant2 || 'Non disponible');
                $('#3gagnat').text(tournament.gagnant3 || 'Non disponible');
                // tableau de user classement score-classement nbr partie
                for (let i = 1; i <= 5; i++) {
                    const idKey = `id${i}`;
                    const classementKey = `classement${i}`;
                    const scoreClassemetKey = `score-classemet${i}`;
                    const nbrPartiKey = `nbr-parti${i}`;

                    if (tournament[idKey]) {
                        $(`#${idKey}`).text(tournament[idKey]);
                        $(`#${classementKey}`).text(getOrdinalSuffix(tournament[classementKey]));
                        $(`#${scoreClassemetKey}`).text(tournament[scoreClassemetKey]);
                        $(`#${nbrPartiKey}`).text(tournament[nbrPartiKey]);
                    }
                }
            }
        },
        error: function(xhr, status, error) {
            console.error("Erreur lors de la récupération des données: ", error);
        }
    });
});