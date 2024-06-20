console.log("pong3D.js chargé");



function loadScript(src) {
    console.log("pong3D.js src=", src);

    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        console.log("pong3D.js src=", src);
        script.onload = () => {
            console.log("Script loaded successfully:", src);
            resolve();
        };
        script.onerror = (error) => {
            console.error("Failed to load script:", src, error);
            reject(error);
        };
        document.head.appendChild(script);
    });
}

loadScript("https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js")

    .then(() => {

    let scene, camera, renderer;
    let table, sol, filet;
    let raquette1, raquette2, balle;
    let ballDirection = new THREE.Vector3(1, 0, 0); // Direction initiale de la balle
    let ballSpeed = 1.5; // Vitesse de la balle
    let scorePlayer1 = 0;
    let scorePlayer2 = 0;
    let maxScore = 5; 

function init() {
        // Initialisation de la scène, de la caméra et du renderer
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 100, 200);
        camera.lookAt(scene.position);

        renderer = new THREE.WebGLRenderer({ alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x000000, 0); // Transparent background
        document.body.appendChild(renderer.domElement);

        // Ajout de lumière
        const ambientLight = new THREE.AmbientLight(0x404040);
        scene.add(ambientLight);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(0, 20, 10);
        scene.add(directionalLight);

         // Création d'une boîte géométrique
        const boxGeometry = new THREE.BoxGeometry(5, 5, 5);
    const boxMaterial = new THREE.MeshBasicMaterial({ color: 0x0640F6 });
    const box = new THREE.Mesh(boxGeometry, boxMaterial);
    scene.add(box);

    
    // Sol
    const solGeometry = new THREE.PlaneGeometry(300, 150);
    const solMaterial = new THREE.MeshLambertMaterial({color: 0x111214});
    sol = new THREE.Mesh(solGeometry, solMaterial);
    sol.rotation.x = -Math.PI / 2;
    scene.add(sol);

    // Table de ping-pong
    const tableGeometry = new THREE.BoxGeometry(274, 5, 152.5); // Dimensions ajustées
    const tableMaterial = new THREE.MeshLambertMaterial({color: 0x0640F6}); // Vert typique pour la table
    table = new THREE.Mesh(tableGeometry, tableMaterial);
    table.position.y = 2.5; // Ajustement pour que le bas de la table touche le sol
    scene.add(table);

    // Filet
    const filetGeometry = new THREE.BoxGeometry(5, 15, 152.5); // Largeur du filet négligeable
    const filetMaterial = new THREE.MeshLambertMaterial({color: 0xffffff});
    filet = new THREE.Mesh(filetGeometry, filetMaterial);
    filet.position.z = 15 / 2; // Hauteur du filet
    scene.add(filet);

    // Dimensions des raquettes
    const raquetteRadius = 15; // Rayon de la raquette
    const raquetteDepth = 5; // Épaisseur de la raquette

    // Matériau des raquettes
    const raquetteMaterial1 = new THREE.MeshLambertMaterial({color: 0x418910}); 
    const raquetteMaterial2 = new THREE.MeshLambertMaterial({color: 0xF70404});
    // Raquette Joueur 1
    const raquette1Geometry = new THREE.CylinderGeometry(raquetteRadius, raquetteRadius, raquetteDepth, 32);
    raquette1 = new THREE.Mesh(raquette1Geometry, raquetteMaterial1);
    raquette1.rotation.z = Math.PI / 2; // Oriente la raquette face à la caméra/au ciel
    raquette1.position.set(-125, 10, 0); // Positionnez la raquette sur le côté gauche de la table
    scene.add(raquette1);

    // Raquette Joueur 2
    const raquette2Geometry = new THREE.CylinderGeometry(raquetteRadius, raquetteRadius, raquetteDepth, 32);
    raquette2 = new THREE.Mesh(raquette2Geometry, raquetteMaterial2);
    raquette2.rotation.z = Math.PI / 2; // Oriente la raquette face à la caméra/au ciel
    raquette2.position.set(125, 10, 0); // Positionnez la raquette sur le côté droit de la table
    scene.add(raquette2);

    // Création de la balle
    const balleGeometry = new THREE.SphereGeometry(5, 32, 32); // Rayon de 7.5 pour une balle de taille visible
    const balleMaterial = new THREE.MeshLambertMaterial({color: 0x08842B}); // Balle blanche
    balle = new THREE.Mesh(balleGeometry, balleMaterial);
    balle.position.set(0, 15, 0); // Position initiale de la balle au-dessus de la table
    scene.add(balle);  
    animate(); // Démarrer l'animation
}


let raquetteRadius = 15; 

let lastHitTime = 0; // Le temps du dernier coup
const hitCooldown = 200; // Temps en millisecondes
function moveBall() {
    balle.position.add(ballDirection.clone().multiplyScalar(ballSpeed));
    const now = Date.now();

// Détection de la collision avec les raquettes
const ballBoundingBox = new THREE.Box3().setFromObject(balle);
const raquette1BoundingBox = new THREE.Box3().setFromObject(raquette1);
const raquette2BoundingBox = new THREE.Box3().setFromObject(raquette2);

if (ballBoundingBox.intersectsBox(raquette1BoundingBox) || ballBoundingBox.intersectsBox(raquette2BoundingBox)) {
ballDirection.reflect(new THREE.Vector3(1, 0, 0.1)).normalize().multiplyScalar(ballSpeed);

lastHitTime = now;
}
if (Math.abs(balle.position.x) >= 137) {

//ballDirection.reflect(new THREE.Vector3(1, 0, 0)); 
ballDirection.reflect(new THREE.Vector3(1, 0, 0)); 
// Limiter la position de la balle aux bords de la table
balle.position.x = Math.sign(balle.position.x) * 137;
// Vérifier si la balle a touché le bord gauche
if (balle.position.x < 0) {

    // Ajouter un point au joueur 2 (le joueur à droite)
    scorePlayer2++;
    document.getElementById("scores").innerHTML = scorePlayer1 + "-" + scorePlayer2;

    console.log("score player1", scorePlayer2);
    
    resetGame();
} 
else if(balle.position.x > 0){

    scorePlayer1++;
    document.getElementById("scores").innerHTML = scorePlayer1 + "-" + scorePlayer2;
    console.log("score player2", scorePlayer1);
    resetGame();
}
 
}
if (balle.position.z >= 75 || balle.position.z <= -75) {

ballDirection.reflect(new THREE.Vector3(0, 0, Math.sign(balle.position.z)));
balle.position.z = THREE.MathUtils.clamp(balle.position.z, -75, 75);
}

}

function resetGame() {
balle.position.set(10, 10, 10);
ballSpeedX = 1;
ballSpeedY = 1;
console.log("scorePlayer1",scorePlayer1);
console.log("scorePlayer1",scorePlayer1);
console.log("maxScore",maxScore);
if (scorePlayer1 >= maxScore )
{
console.log("player 1 a gagne ");
//sendScoresToBackend();
setTimeout(window.location.href = "#page_finale", 5000);

}
else if (scorePlayer2 >= maxScore) 
{
console.log("player 2 a gagne ");
//sendScoresToBackend();

setTimeout(window.location.href = "#page_finale", 5000);
}
   
}
// Déplacement des raquettes
const raquetteSpeed = 2; // Vitesse de déplacement des raquettes

// Fonction de mise à jour du déplacement des raquettes
function updateRaquettes() {
    function updateRaquettes() {
// Mettre à jour le mouvement de la raquette du joueur 1
document.getElementById('player1-movement').innerText = `Player 1: ${Key.isDown(Key.W) ? '↑' : ''} ${Key.isDown(Key.S) ? '↓' : ''}`;

// Mettre à jour le mouvement de la raquette du joueur 2
document.getElementById('player2-movement').innerText = `Player 2: ${Key.isDown(Key.UP_ARROW) ? '↑' : ''} ${Key.isDown(Key.DOWN_ARROW) ? '↓' : ''}`;
}
    if (Key.isDown(Key.S)) { // 
    if (raquette1.position.z < 125 / 2) { // Vérifiez si la raquette dépasse la limite supérieure
        raquette1.position.z += raquetteSpeed;
    }
} else if (Key.isDown(Key.W)) { // 
    if (raquette1.position.z > -125 / 2) { // Vérifiez si la raquette dépasse la limite inférieure
        raquette1.position.z -= raquetteSpeed;
    }
}

// Raquette Joueur 2 (droite)
if (Key.isDown(Key.DOWN_ARROW)) { 
    if (raquette2.position.z < 125 / 2) { // Vérifiez si la raquette dépasse la limite supérieure
        raquette2.position.z += raquetteSpeed;
    }
} else if (Key.isDown(Key.UP_ARROW)) { 
    if (raquette2.position.z > -125 / 2) { // Vérifiez si la raquette dépasse la limite inférieure
        raquette2.position.z -= raquetteSpeed;
    }
    }
}

// Fonction de gestion des touches
const Key = {
    _pressed: {},

    W: 87,
   
    // rest of the Key object definition
    S: 83,
    UP_ARROW: 38,
    DOWN_ARROW: 40,

    isDown: function(keyCode) {
        return this._pressed[keyCode];
    },

    onKeyDown: function(event) {
        this._pressed[event.keyCode] = true;
    },

    onKeyUp: function(event) {
        delete this._pressed[event.keyCode];
    }
};

// Ajouter les écouteurs d'événements pour les touches du clavier
window.addEventListener('keydown', function(event) { Key.onKeyDown(event); }, false);
window.addEventListener('keyup', function(event) { Key.onKeyUp(event); }, false);

function animateText(textMesh) {
// Initialiser la position de départ
let startPosition = textMesh.position.clone();

// Définir la position cible pour l'animation
let targetPosition = new THREE.Vector3(100, 50, -1); // Changer la position cible selon vos besoins

// Durée totale de l'animation (en secondes)
let animationDuration = 2;

// Horloge pour suivre le temps écoulé
let clock = new THREE.Clock();

// Fonction d'animation
function update() {
    // Calculer la progression de l'animation (valeur entre 0 et 1)
    let elapsedTime = clock.getElapsedTime();
    let progress = elapsedTime / animationDuration;
    progress = Math.min(progress, 1); // Assurer que la progression ne dépasse pas 1
    
    // Interpoler entre la position de départ et la position cible en fonction de la progression
    let newPosition = startPosition.clone().lerp(targetPosition, progress);
    
    // Mettre à jour la position du texte
    textMesh.position.copy(newPosition);
    
    // Continuer l'animation jusqu'à ce que la durée soit écoulée
    if (progress < 1) {
        requestAnimationFrame(update);
    }
}

// Démarrer l'animation
update();
}




// Fonction d'animation
function animate() {
    requestAnimationFrame(animate);
    updateRaquettes(); // Mettre à jour les positions des raquettes
    
    moveBall(); // Mettre à jour le mouvement de la balle
    renderer.render(scene, camera);
}

// Gestion du redimensionnement de la fenêtre
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});


init(); // Initialisation du jeu

    })

// function sendScoresToBackend() {
// fetch('/api/party/<pk>', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json',
//     },

//     body: JSON.stringify({
//         scorePlayer1: scorePlayer1,
//         scorePlayer2: scorePlayer2,
//     }),
// })
// .then(response => {
//     if (!response.ok) {
//         throw new Error('Network response was not ok');
//     }
//     return response.json();
// })
// .then(data => {
//     console.log('Scores envoyés avec succès au backend:', data);
// })
// .catch(error => {
//     console.error('Erreur lors de l\'envoi des scores au backend:', error);
// });


    .catch(() => {
        console.log("Erreur lors du chargement de anime.js");
    });
