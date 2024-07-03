console.log('stats.js');

getMenuInfos();

function setupTabEventListeners() {
    console.log('setup tab');
    updateDashboardDisplay(1);
    document.querySelectorAll('.btn-custom-1').forEach(tab => {
      tab.addEventListener('click', function() {
        document.querySelectorAll('.btn-custom-1').forEach(t => t.classList.remove('active'));
        this.classList.add('active');
  
        const gameId = this.getAttribute('data-tab') === 'tab1' ? 1 : 
            this.getAttribute('data-tab') === 'tab2' ? 2 :
            this.getAttribute('data-tab') === 'tab3' ? 3 : 1;
        updateDashboardDisplay(gameId);
      });
    });
};

setupTabEventListeners();

// Function to display ordinal suffix
function getOrdinalSuffix(n) {
    const s = ["ème", "er", "ème", "ème", "ème"];
    const v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
};

//function to convert time
function formatDuration(time_played) {
    if (time_played) {
        const hours = Math.floor(time_played / 3600);
        const minutes = Math.floor((time_played % 3600) / 60);
        const seconds = time_played % 60;
        return `${hours}h ${minutes}m ${seconds}s`;
    }
};

// fetch the 5 best players
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

// fetch the dashboard of the current player
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

// to fetch the 5 last parties played
async function fetchMyLastParties(game_id, user_id) {
    console.log('game id et user id =', game_id, ' ', user_id);
    try {
        const response = await fetch(`api/party/retrievePartyByGame/${game_id}/${user_id}`);
        const myLastParties = await response.json();
        console.log('my last parties =', myLastParties);
        if (myLastParties.status == 'error')
            return null;
        return myLastParties;
    } catch (error) {
        console.error('Error fetching last parties:', error);
        return null;  // Rethrow the error to handle it outside this function if needed
    }
};

// display basic user stats
async function displayUserBasicStats(myLeaderboard) {
    console.log('my leaderborad in display basc stats', myLeaderboard);
    if (myLeaderboard.length > 0) {
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

//display the last 5 last parties played
async function displayLastParties(myLastParties){   // cercle de classement user
    console.log('in display parties : ', myLastParties);
    if (myLastParties.length > 0){
        const data = myLastParties
        for (let i = 0; i < 5; i++) {
            const scoreKey = `score${i}`;
            const timeKey = `time${i}`;
            const adversaryKey = `adversary${i}`;
            const winnerKey = `winner${i}`;
            if (data[i]) {
                $(`#${scoreKey}`).text(data[i].score1);
                console.log('score: ', data[i].score1);
                $(`#${timeKey}`).text(formatDuration(data[i].duration));
                if (data[i].player2 === null)
                    $(`#${adversaryKey}`).text('AI');
                else
                    $(`#${adversaryKey}`).text(data[i].player2.username);
                if (data[i].winner_name === 'player 1')
                    $(`#${winnerKey}`).text('Oui');
                else
                    $(`#${winnerKey}`).text('Non');
            }
        }
    }
    else {
        console.log("Error: no parties to display");
    }
};

// display the 5 best players ranking
async function displayBestRanking(leaderboardData){
    if (leaderboardData.length > 0){
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
        console.log("Error: no ranking to display");
    }
};

// display the whole stats
async function updateDashboardDisplay(gameId) {
    try {
        const myId = await getUserId();
        console.log('myId is ', myId);
        console.log('gameiD ', gameId);
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
    
        const myLastParties = await fetchMyLastParties(gameId, myId);
        console.log('in updateDashboard', myLastParties);
        if (!myLastParties)
            throw new Error('last parties not found');
        await displayLastParties(myLastParties);
    } catch (error) {
        console.error('error in update dashboard', error);
    }
};
