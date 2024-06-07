console.log('AI_TEST.js is loaded');

// variable global pour direction
var DIRECTION = {
    IDLE: 0,
    UP: 1,
    DOWN: 2,
    LEFT: 3,
    RIGHT: 4
};

//les nbr de rounds 
var rounds = [5, 5, 3, 3, 2];

//les couleur qui change pour chaque niveaux
var colors = ['#1abc9c', '#2ecc71', '#3498db', '#8c52ff', '#9b59b6'];
 
//creer un objet ball
var Ball = {
    new: function (incrementedSpeed) {//constructeur pour creer des nouveau ball
        return {
            width: 40,
            height: 40,
            x: (this.canvas.width / 2) - 9,//position horizontal(canavas c'est une balise utulise dans html c'est le cadre de jeux dans notre jeux pingpong)
            y: (this.canvas.height / 2) - 9,//position vertical
            moveX: DIRECTION.IDLE,//direction horizontal
            moveY: DIRECTION.IDLE,//direction vertical
            speed: incrementedSpeed || 7 //vitesse ou bien 7 ou bien la valleur passe dans la fct incrementedSpeed
        };
    }
};

// l'Intelligence Artificielle (AI) d'un joueur dans le jeu de Pong
var Ai = {
    new: function (side) {
        var xPosition;//position horizontal initial
        if (side === 'left') {
            xPosition = 150;
        } else {
            xPosition = this.canvas.width - 150;
        }
        return {
            width: 18,
            height: 180,
            x: xPosition,
            y: (this.canvas.height / 2) - 35,//position vertical initial
            score: 0,
            move: DIRECTION.IDLE,
            speed: 8
        };
    }
};

/*querySelector:Renvoie le premier noeud Element correspondant dans la sous-arborescence du noeud
. Si aucun noeud correspondant n'est trouvé, null est renvoyé.*/
var Game = {
    initialize: function () {
        this.canvas = document.querySelector('canvas');//chercher vanvas dans fichier html et le stocker
        this.context = this.canvas.getContext('2d');//obtient le contexte de jeux 2d  permet de dessiner des formes
 
        this.canvas.width = 1400;
        this.canvas.height = 1000;
        
        /*style.width :la largeur définie via les styles CSS*/ 
        this.canvas.style.width = (this.canvas.width / 2 ) + 'px';
        this.canvas.style.height = (this.canvas.height / 2) + 'px';
        /* call c'est pour appeler la fct et initialiser son objet */
        this.player = Ai.new.call(this, 'left');//le player (moi) 
        this.ai = Ai.new.call(this, 'right');//c'est pour ordinateur
        this.ball = Ball.new.call(this);
 
        this.ai.speed = 5;//vitesse definis a 5
        this.running = this.over = false;//en cours
        this.turn = this.ai;//tour
        this.timer = this.round = 0;//compteur
        this.color = '#8c52ff';//couleur de bas 
 
        Pong.menu();
        Pong.listen();
    },
 
    endGameMenu: function (text) {
        // Change the canvas font size and color
        Pong.context.font = '45px Courier New';
        Pong.context.fillStyle = this.color;
 
        // Draw the rectangle behind the 'Press any key to begin' text.
        Pong.context.fillRect(
            Pong.canvas.width / 2 - 350,
            Pong.canvas.height / 2 - 48,700,100
        );
 
        // Change the canvas color;
        Pong.context.fillStyle = '#ffffff';
 
        // Draw the end game menu text ('Game Over' and 'Winner')
        Pong.context.fillText(text,
            Pong.canvas.width / 2,
            Pong.canvas.height / 2 + 15
        );
 
        setTimeout(function () {
            Pong = Object.assign({}, Game);
            Pong.initialize();
        }, 3000);
    },
 
    menu: function () {
        // Draw all the Pong objects in their current state
        Pong.draw();
 
        // Change the canvas font size and color
        this.context.font = '50px Courier New';
        this.context.fillStyle = this.color;
 
        // Draw the rectangle behind the 'Press any key to begin' text.
        this.context.fillRect(
            this.canvas.width / 2 - 350,
            this.canvas.height / 2 - 48,
            700,
            100
        );
 
        // Change the canvas color;
        this.context.fillStyle = '#ffffff';
 
        // Draw the 'press any key to begin' text
        this.context.fillText('Press any key to begin',
            this.canvas.width / 2,
            this.canvas.height / 2 + 15
        );
    },
 
    // Update all objects (move the player, ai, ball, increment the score, etc.)
    update: function () {
        if (!this.over) {
            // If the ball collides with the bound limits - correct the x and y coords.
            if (this.ball.x <= 0) Pong._resetTurn.call(this, this.ai, this.player);
            if (this.ball.x >= this.canvas.width - this.ball.width) Pong._resetTurn.call(this, this.player, this.ai);
            if (this.ball.y <= 0) this.ball.moveY = DIRECTION.DOWN;
            if (this.ball.y >= this.canvas.height - this.ball.height) this.ball.moveY = DIRECTION.UP;
 
            // Move player if they player.move value was updated by a keyboard event
            if (this.player.move === DIRECTION.UP) this.player.y -= this.player.speed;
            else if (this.player.move === DIRECTION.DOWN) this.player.y += this.player.speed;
 
            // On new serve (start of each turn) move the ball to the correct side
            // and randomize the direction to add some challenge.
            if (Pong._turnDelayIsOver.call(this) && this.turn) {
                this.ball.moveX = this.turn === this.player ? DIRECTION.LEFT : DIRECTION.RIGHT;
                this.ball.moveY = [DIRECTION.UP, DIRECTION.DOWN][Math.round(Math.random())];
                this.ball.y = Math.floor(Math.random() * this.canvas.height - 200) + 200;
                this.turn = null;
            }
 
            // If the player collides with the bound limits, update the x and y coords.
            if (this.player.y <= 0) this.player.y = 0;
            else if (this.player.y >= (this.canvas.height - this.player.height)) this.player.y = (this.canvas.height - this.player.height);
 
            // Move ball in intended direction based on moveY and moveX values
            if (this.ball.moveY === DIRECTION.UP) this.ball.y -= (this.ball.speed / 1.5);
            else if (this.ball.moveY === DIRECTION.DOWN) this.ball.y += (this.ball.speed / 1.5);
            if (this.ball.moveX === DIRECTION.LEFT) this.ball.x -= this.ball.speed;
            else if (this.ball.moveX === DIRECTION.RIGHT) this.ball.x += this.ball.speed;
 
            // Handle ai (AI) UP and DOWN movement
            if (this.ai.y > this.ball.y - (this.ai.height / 2)) {
                if (this.ball.moveX === DIRECTION.RIGHT) this.ai.y -= this.ai.speed / 1.5;
                else this.ai.y -= this.ai.speed / 4;
            }
            if (this.ai.y < this.ball.y - (this.ai.height / 2)) {
                if (this.ball.moveX === DIRECTION.RIGHT) this.ai.y += this.ai.speed / 1.5;
                else this.ai.y += this.ai.speed / 4;
            }
 
            // Handle ai (AI) wall collision
            if (this.ai.y >= this.canvas.height - this.ai.height) this.ai.y = this.canvas.height - this.ai.height;
            else if (this.ai.y <= 0) this.ai.y = 0;
 
            // Handle Player-Ball collisions
            if (this.ball.x - this.ball.width <= this.player.x && this.ball.x >= this.player.x - this.player.width) {
                if (this.ball.y <= this.player.y + this.player.height && this.ball.y + this.ball.height >= this.player.y) {
                    this.ball.x = (this.player.x + this.ball.width);
                    this.ball.moveX = DIRECTION.RIGHT;
 
                }
            }
 
            // Handle ai-ball collision
            if (this.ball.x - this.ball.width <= this.ai.x && this.ball.x >= this.ai.x - this.ai.width) {
                if (this.ball.y <= this.ai.y + this.ai.height && this.ball.y + this.ball.height >= this.ai.y) {
                    this.ball.x = (this.ai.x - this.ball.width);
                    this.ball.moveX = DIRECTION.LEFT;
 
                }
            }
        }
 
        // Handle the end of round transition
        // Check to see if the player won the round.
        if (this.player.score === rounds[this.round]) {
            // Check to see if there are any more rounds/levels left and display the victory screen if
            // there are not.
            if (!rounds[this.round + 1]) {
                this.over = true;
                setTimeout(function () { Pong.endGameMenu('Winner!'); }, 1000);
            } else {
                // If there is another round, reset all the values and increment the round number.
                this.color = this._generateRoundColor();
                this.player.score = this.ai.score = 0;
                this.player.speed += 0.5;
                this.ai.speed += 1;
                this.ball.speed += 1;
                this.round += 1;
 
            }
        }
        // Check to see if the ai/AI has won the round.
        else if (this.ai.score === rounds[this.round]) {
            this.over = true;
            setTimeout(function () { Pong.endGameMenu('Game Over!'); }, 1000);
        }
    },
 
    // Draw the objects to the canvas element
    draw: function () {
        // Clear the Canvas
        this.context.clearRect(
            0,
            0,
            this.canvas.width,
            this.canvas.height
        );
 
        // Set the fill style to black
        this.context.fillStyle = this.color;
 
        // Draw the background
        this.context.fillRect(
            0,
            0,
            this.canvas.width,
            this.canvas.height
        );
 
        // Set the fill style to white (For the paddles and the ball)
        this.context.fillStyle = '#ffffff';
 
        // Draw the Player
        this.context.fillRect(
            this.player.x,
            this.player.y,
            this.player.width,
            this.player.height
        );
 
        // Draw the Ai
        this.context.fillRect(
            this.ai.x,
            this.ai.y,
            this.ai.width,
            this.ai.height 
        );
 
        // Draw the Ball
        if (Pong._turnDelayIsOver.call(this)) {
            this.context.fillRect(
                this.ball.x,
                this.ball.y,
                this.ball.width,
                this.ball.height
            );
        }
 
        // Draw the net (Line in the middle)
        this.context.beginPath();
        this.context.setLineDash([30, 15]);
        this.context.moveTo((this.canvas.width / 2), this.canvas.height - 14);
        this.context.lineTo((this.canvas.width / 2), 100);
        this.context.lineWidth = 10;
        this.context.strokeStyle = '#ffffff';
        this.context.stroke();
 
        // Set the default canvas font and align it to the center
        this.context.font = '100px Courier New';
        this.context.textAlign = 'center';
 
        // Draw the players score (left)
        this.context.fillText(
            this.player.score.toString(),
            (this.canvas.width / 2) - 300,
            200
        );
 
        // Draw the paddles score (right)
        this.context.fillText(
            this.ai.score.toString(),
            (this.canvas.width / 2) + 300,
            200
        );
 
        // Change the font size for the center score text
        this.context.font = '30px Courier New';
 
        // Draw the winning score (center)
        this.context.fillText(
            'Round ' + (Pong.round + 1),
            (this.canvas.width / 2),
            35
        );
 
        // Change the font size for the center score value
        this.context.font = '40px Courier';
 
        // Draw the current round number
        this.context.fillText(
            rounds[Pong.round] ? rounds[Pong.round] : rounds[Pong.round - 1],
            (this.canvas.width / 2),
            100
        );
    },
 
    loop: function () {
        Pong.update();
        Pong.draw();
 
        // If the game is not over, draw the next frame.
        if (!Pong.over) requestAnimationFrame(Pong.loop);
    },
 
    listen: function () {
        document.addEventListener('keydown', function (key) {
            // Handle the 'Press any key to begin' function and start the game.
            if (Pong.running === false) {
                Pong.running = true;
                window.requestAnimationFrame(Pong.loop);
            }
 
            // Handle up arrow and w key events
            if (key.keyCode === 38 || key.keyCode === 87) Pong.player.move = DIRECTION.UP;
 
            // Handle down arrow and s key events
            if (key.keyCode === 40 || key.keyCode === 83) Pong.player.move = DIRECTION.DOWN;
        });
 
        // Stop the player from moving when there are no keys being pressed.
        document.addEventListener('keyup', function (key) { Pong.player.move = DIRECTION.IDLE; });
    },
 
    // Reset the ball location, the player turns and set a delay before the next round begins.
    _resetTurn: function(victor, loser) {
        this.ball = Ball.new.call(this, this.ball.speed);
        this.turn = loser;
        this.timer = (new Date()).getTime();
 
        victor.score++;
    },
 
    // Wait for a delay to have passed after each turn.
    _turnDelayIsOver: function() {
        return ((new Date()).getTime() - this.timer >= 1000);
    },
 
    // Select a random color as the background of each level/round.
    _generateRoundColor: function () {
        var newColor = colors[Math.floor(Math.random() * colors.length)];
        if (newColor === this.color) return Pong._generateRoundColor();
        return newColor;
    }
};
 
var Pong = Object.assign({}, Game);
Pong.initialize();

function startGame() {
    Pong.running = true;
    window.requestAnimationFrame(Pong.loop);
    startButton.disabled = true;
    stopButton.disabled = false;
  }
  
  function stopGame() {
    Pong.running = false;
    stopButton.disabled = true;
    startButton.disabled = false;
  }
  
  const startButton = document.getElementById('startButton');
  const stopButton = document.getElementById('stopButton');
  
  if (startButton) {
    startButton.addEventListener('click', startGame);
  }
  
  if (stopButton) {
    stopButton.addEventListener('click', stopGame);
  }