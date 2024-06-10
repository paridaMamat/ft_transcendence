console.log("in lobby.js");

getMenuInfos(); // for the latral menu

async function enterLobby(){
    const response = await fetch ('');
    if (response.ok){

    } else {
        console.error('Error fetching user info for lobby:', response.statusText);
    }
}

// 1- des qu'on clique sur un jeu, on entre dans le lobby
// 2- ca cree un nouveau lobby et ca envoie l'info dans la database 

// fonction pour envoi de username + avatar lorsqu'on a trouve l'adversaire
// avec l'algo python.