console.log("game.js loaded");


var renderer, scene, camera, pointLight, spotLight;

var fieldWidth = 800, fieldHeight = 300;

var paddleWidth, paddleHeight, paddleDepth, paddleQuality;
var paddle1DirY = 0, paddle2DirY = 0, paddleSpeed = 10;

var ball, paddle1, paddle2;
var ballDirX = 1, ballDirY = 1, ballSpeed = 3;

var score1 = 0, score2 = 0;
var maxScore = 7;

var difficulty = 0.2;


// Initialisation du jeu

function setup()
{
	document.getElementById("winnerBoard").innerHTML = "First to " + maxScore + " wins!";
	
	score1 = 0;
	score2 = 0;
	
	createScene();
	
	draw();
}
// Création de la scène 3D
function createScene()
{
	var WIDTH = 1000,
	  HEIGHT = 1000;

	var VIEW_ANGLE = 70,
	  ASPECT = WIDTH / HEIGHT,
	  NEAR = 0.1,
	  FAR = 10000;

	var c = document.getElementById("gameCanvas");


	renderer = new THREE.WebGLRenderer({ alpha: true });
	renderer.setClearColor(0x000000, 0);
	camera =
	  new THREE.PerspectiveCamera(VIEW_ANGLE,ASPECT,NEAR,FAR);
	  //camera.lookAt()
	scene = new THREE.Scene();

	
	scene.add(camera);
	
	camera.position.z = 320;
	//camera.lookAt()

	renderer.setSize(WIDTH, HEIGHT);

	c.appendChild(renderer.domElement);

	// Création du plateau de jeu
	var planeWidth = fieldWidth,
		planeHeight = fieldHeight,
		planeQuality = 10;
		
  // Matériaux pour les raquettes et la balle
	var paddle1Material = new THREE.MeshLambertMaterial({color: 0x1B32C0});
	var paddle2Material = new THREE.MeshLambertMaterial({color: 0xFF0000});
	
	var planeMaterial =new THREE.MeshLambertMaterial({color: 0x4BD121});

	var tableMaterial =new THREE.MeshLambertMaterial({ color: 0x534d0d});

	var pillarMaterial =new THREE.MeshLambertMaterial({color: 0x534d0d});
	
	var groundMaterial =new THREE.MeshLambertMaterial({color: 0x888888});	
	
	// creation de surfac
	var plane = new THREE.Mesh(new THREE.PlaneGeometry(planeWidth * 0.95,planeHeight,planeQuality,planeQuality),planeMaterial);
	  
	scene.add(plane);
	plane.receiveShadow = true;	
	
	var table = new THREE.Mesh(new THREE.CubeGeometry(planeWidth * 1.05,planeHeight * 1.03,100,	planeQuality,planeQuality,1),tableMaterial);
	table.position.z = -51;	
	scene.add(table);
	table.receiveShadow = true;	
		
	var radius = 5,
		segments = 6,
		rings = 6;
	var sphereMaterial =new THREE.MeshLambertMaterial({color: 0xD43001});
		
	ball = new THREE.Mesh(new THREE.SphereGeometry(radius,segments,rings), sphereMaterial);

	scene.add(ball);
	
	ball.position.x = 0;
	ball.position.y = 0;
	ball.position.z = radius;
	ball.receiveShadow = true;
    ball.castShadow = true;
	// Dimensions des raquettes
	paddleWidth = 20;
	paddleHeight = 60;
	paddleDepth = 10;
	paddleQuality = 10;
		
	paddle1 = new THREE.Mesh(new THREE.CubeGeometry(paddleWidth,paddleHeight,paddleDepth,paddleQuality,paddleQuality,paddleQuality), paddle1Material);

	scene.add(paddle1);
	paddle1.receiveShadow = true;
    paddle1.castShadow = true;
	
	paddle2 = new THREE.Mesh(

	new THREE.CubeGeometry(paddleWidth,paddleHeight,paddleDepth,paddleQuality,paddleQuality,paddleQuality),paddle2Material);
	  
	scene.add(paddle2);
	paddle2.receiveShadow = true;
    paddle2.castShadow = true;	
	
	paddle1.position.x = -fieldWidth/2 + paddleWidth;
	paddle2.position.x = fieldWidth/2 - paddleWidth;
	
	paddle1.position.z = paddleDepth;
	paddle2.position.z = paddleDepth;
	// Ajout des piliers décoratifs
	
	for (var i = 0; i < 5; i++)
	{
		var backdrop = new THREE.Mesh(new THREE.CubeGeometry( 30, 30, 300, 1, 1,1 ),pillarMaterial);
		  
		backdrop.position.x = -50 + i * 100;
		backdrop.position.y = 230;
		backdrop.position.z = -30;		
		backdrop.castShadow = true;
		backdrop.receiveShadow = true;		  
		scene.add(backdrop);	
	}
	
	for (var i = 0; i < 5; i++)
	{
		var backdrop = new THREE.Mesh(new THREE.CubeGeometry( 30, 30, 300, 1, 1,1 ),pillarMaterial);
		  
		backdrop.position.x = -50 + i * 100;
		backdrop.position.y = -230;
		backdrop.position.z = -30;
		backdrop.castShadow = true;
		backdrop.receiveShadow = true;		
		scene.add(backdrop);	
	}
	

	var ground = new THREE.Mesh(new THREE.CubeGeometry( 1000, 1000, 3, 1, 1, 1 ),groundMaterial);
 
	ground.position.z = -132;
	ground.receiveShadow = true;	
	scene.add(ground);		
		
	// // create a point light
	pointLight =new THREE.PointLight(0xF8D898);

	// sposition
	pointLight.position.x = -1000;
	pointLight.position.y = 0;
	pointLight.position.z = 1000;
	pointLight.intensity = 2.9;
	pointLight.distance = 10000;
	
	scene.add(pointLight);
		
	
    spotLight = new THREE.SpotLight(0xF8D898);
    spotLight.position.set(0, 0, 460);
    spotLight.intensity = 1.5;
    spotLight.castShadow = true;
    scene.add(spotLight);
	
	renderer.shadowMapEnabled = true;		
}
// Fonction qui dessine et anime le jeu
function draw()
{	
	// Rafrîchissement de la scène
	renderer.render(scene, camera);
	// Réglage des positions et des mouvements

	ballPhysics();
	paddlePhysics();
	cameraPhysics();
	// Mise à jour de la position des raquettes
	playerPaddleMovement();
	opponentPaddleMovement();
	// Animation de la prochaine image
	requestAnimationFrame(draw);
}

function ballPhysics()
{
	if (ball.position.x <= -fieldWidth/2)
	{	
		score2++;
		document.getElementById("scores").innerHTML = score1 + "-" + score2;
		resetBall(2);
		matchScoreCheck();	
	}
	
	if (ball.position.x >= fieldWidth/2)
	{	
		score1++;
		document.getElementById("scores").innerHTML = score1 + "-" + score2;
		resetBall(1);
		matchScoreCheck();	
	}
	
	if (ball.position.y <= -fieldHeight/2)
	{
		ballDirY = -ballDirY;
		// Limiter la vitesse de la balle après un rebond sur le haut
		 ballDirY = Math.min(ballDirY, ballSpeed);
	}	
	if (ball.position.y >= fieldHeight/2)
	{
		ballDirY = -ballDirY;
		// Limiter la vitesse de la balle après un rebond sur le bas
        ballDirY = Math.max(ballDirY, -ballSpeed);
	}
	
	ball.position.x += ballDirX * ballSpeed;
	ball.position.y += ballDirY * ballSpeed;

	if (ballDirY > ballSpeed * 2)
	{
		ballDirY = ballSpeed * 2;
	}
	else if (ballDirY < -ballSpeed * 2)
	{
		ballDirY = -ballSpeed * 2;
	}
}
// Logique des mouvements de la raquette de l'adversaire

function opponentPaddleMovement() {
    // Si la balle se déplace vers le CPU (direction positive sur l'axe X)
    if (ballDirX > 0) {
        // L'IA se déplace vers la position anticipée de la balle sur l'axe Y
        var targetY = ball.position.y;
        // Lerp vers la position de la balle avec une certaine vitesse (difficulty)
        paddle2DirY = (targetY - paddle2.position.y) * difficulty;
    } else {
        // Si la balle se déplace vers le joueur, l'IA revient à une position neutre
        // Cela peut être une position au milieu du terrain ou une autre position de défense
        var neutralY = 0; // Position neutre sur l'axe Y
        paddle2DirY = (neutralY - paddle2.position.y) * difficulty;
    }

    // Limiter la vitesse de déplacement de la raquette de l'ordinateur
    if (Math.abs(paddle2DirY) <= paddleSpeed) {
        paddle2.position.y += paddle2DirY;
    } else {
        paddle2.position.y += paddleSpeed * Math.sign(paddle2DirY);
    }
    
    // Lerp pour revenir à l'échelle normale
    paddle2.scale.y += (1 - paddle2.scale.y) * 0.2;
}



// Logique des mouvements de la raquette du joueur
function playerPaddleMovement()
{
	// move left
	if (Key.isDown(Key.A))		
	{
		
		if (paddle1.position.y < fieldHeight * 0.45)
		{
			paddle1DirY = paddleSpeed * 0.5;
		}
		
		else
		{
			paddle1DirY = 0;
			paddle1.scale.z += (10 - paddle1.scale.z) * 0.2;
		}
	}	
	else if (Key.isDown(Key.D))
	{
	
		if (paddle1.position.y > -fieldHeight * 0.45)
		{
			paddle1DirY = -paddleSpeed * 0.5;
		}
	
		else
		{
			paddle1DirY = 0;
			paddle1.scale.z += (10 - paddle1.scale.z) * 0.2;
		}
	}
	else
	{
		paddle1DirY = 0;
	}
	
	paddle1.scale.y += (1 - paddle1.scale.y) * 0.2;	
	paddle1.scale.z += (1 - paddle1.scale.z) * 0.2;	
	paddle1.position.y += paddle1DirY;
}
// Logique de la caméra

function cameraPhysics()
{
	spotLight.position.x = ball.position.x * 2;
	spotLight.position.y = ball.position.y * 2;
	
	camera.position.x = paddle1.position.x - 100;
	camera.position.y += (paddle1.position.y - camera.position.y) * 0.05;
	camera.position.z = paddle1.position.z + 100 + 0.04 * (-ball.position.x + paddle1.position.x);
	
	camera.rotation.x = -0.01 * (ball.position.y) * Math.PI/180;
	camera.rotation.y = -60 * Math.PI/180;
	camera.rotation.z = -90 * Math.PI/180;
}

// Logique des collisions de la raquette
function paddlePhysics() {
    
    if (ball.position.x <= paddle1.position.x + paddleWidth && ball.position.x >= paddle1.position.x) {
        // Vérifie si la balle est alignée avec la raquette sur l'axe des y
        if (ball.position.y <= paddle1.position.y + paddleHeight / 2 && ball.position.y >= paddle1.position.y - paddleHeight / 2) {
            // Si c'est le cas, inverse la direction X et modifie sa direction Y en fonction de l'endroit où elle frappe la raquette
            ballDirX = -ballDirX;
            var deltaY = ball.position.y - paddle1.position.y;
            ballDirY += deltaY * 0.07;
        }
    }

    // LOGIQUE DE LA RAQUETTE DE L'ADVERSAIRE

    // Même logique que ci-dessus, mais pour la raquette2
    if (ball.position.x >= paddle2.position.x - paddleWidth && ball.position.x <= paddle2.position.x) {
        // Vérifie l'alignement avec la raquette sur l'axe des y
        if (ball.position.y <= paddle2.position.y + paddleHeight / 2 && ball.position.y >= paddle2.position.y - paddleHeight / 2) {
            // Inverse la direction X et modifie la direction Y en fonction de l'endroit où elle frappe la raquette
            ballDirX = -ballDirX;
            var deltaY = ball.position.y - paddle2.position.y;
            ballDirY += deltaY * 0.07;
        }
    }
}

// Réinitialisation de la balle après un point

function resetBall(loser)
{

	ball.position.x = 0;
	ball.position.y = 0;
	
	// Direction de la balle en fonction du gagnant du point
	if (loser == 1)
	{
		ballDirX = -1;
	}
	
	else
	{
		ballDirX = 1;
	}
	
	
	ballDirY = 1;
}

var bounceTime = 0;
//verifier le matsh sa se finit a 7 points
function matchScoreCheck()
{
	if (score1 >= maxScore)
	{
		
		ballSpeed = 0;

		document.getElementById("scoresdddd").innerHTML = "Player wins!";		
		document.getElementById("winnerBoard").innerHTML = "Refresh to play again";
	
		bounceTime++;
		paddle1.position.z = Math.sin(bounceTime * 0.1) * 10;
		
		paddle1.scale.z = 2 + Math.abs(Math.sin(bounceTime * 0.1)) * 10;
		paddle1.scale.y = 2 + Math.abs(Math.sin(bounceTime * 0.05)) * 10;
	}

	else if (score2 >= maxScore)
	{
		ballSpeed = 0;
		document.getElementById("scores").innerHTML = "CPU wins!";
		document.getElementById("winnerBoard").innerHTML = "Refresh to play again";
		bounceTime++;
		paddle2.position.z = Math.sin(bounceTime * 0.1) * 10;
		paddle2.scale.z = 2 + Math.abs(Math.sin(bounceTime * 0.1)) * 10;
		paddle2.scale.y = 2 + Math.abs(Math.sin(bounceTime * 0.05)) * 10;
	}
}