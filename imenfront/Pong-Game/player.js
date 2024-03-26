// variable globale pour les directions
var DIRECTION = {
    IDLE: 0,
    UP: 1,
    DOWN: 2,
    LEFT: 3,
    RIGHT: 4
};

// les nombres de rounds
var rounds = [5, 5, 3, 3, 2];

// les couleurs qui changent pour chaque niveau
var colors = ['#1abc9c', '#2ecc71', '#3498db', '#8c52ff', '#9b59b6'];

// créer un objet ball
var Ball = {
    new: function (incrementedSpeed, player1StartPosition, player2StartPosition) {
        return {
            width: 18,
            height: 18,
            x: (this.canvas.width / 2) - 9,
            y: (this.canvas.height / 2) - 9,
            moveX: DIRECTION.IDLE,
            moveY: DIRECTION.IDLE,
            speed: incrementedSpeed || 5,
            player1StartPosition: player1StartPosition,
            player2StartPosition: player2StartPosition
        };
    }
};

// Créer un objet Player pour chaque joueur
var Player = {
    new: function (side, startPosition) {
        return {
            width: 18,
            height: 180,
            x: (side === 'left') ? 150 : this.canvas.width - 150,
            y: startPosition,
            score: 0,
            move: DIRECTION.IDLE,
            speed: 8
        };
    }
};



var Game = {
    initialize: function () {
        this.canvas = document.querySelector('canvas');
        this.context = this.canvas.getContext('2d');

        this.canvas.width = 1400;
        this.canvas.height = 800;
        
        this.canvas.style.width = (this.canvas.width / 2) + 'px';
        this.canvas.style.height = (this.canvas.height / 2) + 'px';

        this.player1 = Player.new.call(this, 'left', 150);
        this.player2 = Player.new.call(this, 'right', this.canvas.width - 150);
        this.ball = Ball.new.call(this);
        this.running = this.over = false;
        this.turn = null;
        this.timer = this.round = 0;
        this.color = '#8c52ff';

        this.menu();
        this.listen();
        this.startBall();
    },

    endGameMenu: function (text) {
        this.context.font = '45px Courier New';
        this.context.fillStyle = this.color;

        this.context.fillRect(
            this.canvas.width / 2 - 350,
            this.canvas.height / 2 - 48,
            700,
            100
        );

        this.context.fillStyle = '#ffffff';

        this.context.fillText(text,
            this.canvas.width / 2,
            this.canvas.height / 2 + 15
        );

        setTimeout(function () {
            Pong = Object.assign({}, Game);
            Pong.initialize();
        }, 3000);
    },

    startBall: function() {
        var direction = Math.random() < 0.5 ? DIRECTION.LEFT : DIRECTION.RIGHT;
        this.ball.moveX = direction;
        this.ball.moveY = [DIRECTION.UP, DIRECTION.DOWN][Math.round(Math.random())];
        this.ball.y = Math.floor(Math.random() * (this.canvas.height - this.ball.height));
    },
    
    
    menu: function () {
        this.draw();

        this.context.font = '50px Courier New';
        this.context.fillStyle = this.color;

        this.context.fillRect(
            this.canvas.width / 2 - 350,
            this.canvas.height / 2 - 48,
            700,
            100
        );

        this.context.fillStyle = '#ffffff';

        this.context.fillText('Press any key to begin',
            this.canvas.width / 2,
            this.canvas.height / 2 + 15
        );
    },

    update: function () {
        if (!this.over) {
            if (this.ball.x <= 0) this._resetTurn.call(this, this.player2);
            if (this.ball.x >= this.canvas.width - this.ball.width) this._resetTurn.call(this, this.player1);
            if (this.ball.y <= 0) this.ball.moveY = DIRECTION.DOWN;
            if (this.ball.y >= this.canvas.height - this.ball.height) this.ball.moveY = DIRECTION.UP;

            if (this.player1.move === DIRECTION.UP) this.player1.y -= this.player1.speed;
            else if (this.player1.move === DIRECTION.DOWN) this.player1.y += this.player1.speed;

            if (this.player2.move === DIRECTION.UP) this.player2.y -= this.player2.speed;
            else if (this.player2.move === DIRECTION.DOWN) this.player2.y += this.player2.speed;

            if (this._turnDelayIsOver.call(this) && this.turn) {
                this.ball.moveX = this.turn === this.player1 ? DIRECTION.LEFT : DIRECTION.RIGHT;
                this.ball.moveY = [DIRECTION.UP, DIRECTION.DOWN][Math.round(Math.random())];
                this.ball.y = Math.floor(Math.random() * this.canvas.height - 200) + 200;
                this.turn = null;
            }

            if (this.player1.y <= 0) this.player1.y = 0;
            else if (this.player1.y >= (this.canvas.height - this.player1.height)) this.player1.y = (this.canvas.height - this.player1.height);

            if (this.player2.y <= 0) this.player2.y = 0;
            else if (this.player2.y >= (this.canvas.height - this.player2.height)) this.player2.y = (this.canvas.height - this.player2.height);

            if (this.ball.moveY === DIRECTION.UP) this.ball.y -= (this.ball.speed / 1.5);
            else if (this.ball.moveY === DIRECTION.DOWN) this.ball.y += (this.ball.speed / 1.5);
            if (this.ball.moveX === DIRECTION.LEFT) this.ball.x -= this.ball.speed;
            else if (this.ball.moveX === DIRECTION.RIGHT) this.ball.x += this.ball.speed;

            if (this.ball.x - this.ball.width <= this.player1.x && this.ball.x >= this.player1.x - this.player1.width) {
                if (this.ball.y <= this.player1.y + this.player1.height && this.ball.y + this.ball.height >= this.player1.y) {
                    this.ball.x = (this.player1.x + this.ball.width);
                    this.ball.moveX = DIRECTION.RIGHT;
                }
            }

            if (this.ball.x - this.ball.width <= this.player2.x && this.ball.x >= this.player2.x - this.player2.width) {
                if (this.ball.y <= this.player2.y + this.player2.height && this.ball.y + this.ball.height >= this.player2.y) {
                    this.ball.x = (this.player2.x - this.ball.width);
                    this.ball.moveX = DIRECTION.LEFT;
                }
            }
        }

        if (this.player1.score === rounds[this.round]) {
            if (!rounds[this.round + 1]) {
                this.over = true;
                setTimeout(function () { Pong.endGameMenu('Player 1 Wins!'); }, 1000);
            } else {
                this.color = this._generateRoundColor();
                this.player1.score = this.player2.score = 0;
                this.player1.speed += 0.5;
                this.player2.speed += 0.5;
                this.ball.speed += 1;
                this.round += 1;
            }
        } else if (this.player2.score === rounds[this.round]) {
            this.over = true;
            setTimeout(function () { Pong.endGameMenu('Player 2 Wins!'); }, 1000);
        }
    },

    draw: function () {
        this.context.clearRect(
            0,
            0,
            this.canvas.width,
            this.canvas.height
        );

        this.context.fillStyle = this.color;

        this.context.fillRect(
            0,
            0,
            this.canvas.width,
            this.canvas.height
        );

        this.context.fillStyle = '#ffffff';

        this.context.fillRect(
            this.player1.x,
            this.player1.y,
            this.player1.width,
            this.player1.height
        );

        this.context.fillRect(
            this.player2.x,
            this.player2.y,
            this.player2.width,
            this.player2.height
        );

        if (this._turnDelayIsOver.call(this)) {
            this.context.fillRect(
                this.ball.x,
                this.ball.y,
                this.ball.width,
                this.ball.height
            );
        }

        this.context.beginPath();
        this.context.setLineDash([7, 15]);
        this.context.moveTo((this.canvas.width / 2), this.canvas.height - 140);
        this.context.lineTo((this.canvas.width / 2), 140);
        this.context.lineWidth = 10;
        this.context.strokeStyle = '#ffffff';
        this.context.stroke();

        this.context.font = '100px Courier New';
        this.context.textAlign = 'center';

        this.context.fillText(
            this.player1.score.toString(),
            (this.canvas.width / 2) - 300,
            200
        );

        this.context.fillText(
            this.player2.score.toString(),
            (this.canvas.width / 2) + 300,
            200
        );

        this.context.font = '30px Courier New';

        this.context.fillText(
            'Round ' + (this.round + 1),
            (this.canvas.width / 2),
            35
        );

        this.context.font = '40px Courier';

        this.context.fillText(
            rounds[Pong.round] ? rounds[Pong.round] : rounds[Pong.round - 1],
            (this.canvas.width / 2),
            100
        );
    },

    loop: function () {
        Pong.update();
        Pong.draw();

        if (!Pong.over) requestAnimationFrame(Pong.loop);
    },

    listen: function () {
        var self = this;

        document.addEventListener('keydown', function (key) {
            if (self.running === false) {
                self.running = true;
                window.requestAnimationFrame(self.loop);
            }

            // Player 1 controls
            if (key.keyCode === 87) self.player1.move = DIRECTION.UP; // W key for up
            if (key.keyCode === 83) self.player1.move = DIRECTION.DOWN; // S key for down

            // Player 2 controls
            if (key.keyCode === 38) self.player2.move = DIRECTION.UP; // Up arrow key for up
            if (key.keyCode === 40) self.player2.move = DIRECTION.DOWN; // Down arrow key for down
        });

        document.addEventListener('keyup', function (key) {
            // Player 1 controls
            if (key.keyCode === 87 || key.keyCode === 83) self.player1.move = DIRECTION.IDLE;

            // Player 2 controls
            if (key.keyCode === 38 || key.keyCode === 40) self.player2.move = DIRECTION.IDLE;
        });
    },

    _resetTurn: function (victor) {
        this.ball = Ball.new.call(this, this.ball.speed, this.player1.y, this.player2.y);
        this.turn = null;
        this.timer = (new Date()).getTime();

        victor.score++;
        this.startBall();
    },

    _turnDelayIsOver: function () {
        return ((new Date()).getTime() - this.timer >= 1000);
    },

    _generateRoundColor: function () {
        var newColor = colors[Math.floor(Math.random() * colors.length)];
        if (newColor === this.color) return Pong._generateRoundColor();
        return newColor;
    }
};

var Pong = Object.assign({}, Game);
Pong.initialize();
