import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Button from "../../components/button/Button";
import 'bootstrap/dist/css/bootstrap.min.css';
import Game from '../../game/Game';
import { KeyboardControls } from '@react-three/drei';
import { Canvas } from '@react-three/fiber';
import { useTranslation } from 'react-i18next';


function TournamentBracket() {
  const { tournamentid } = useParams();
  const [tournament, setTournament] = useState(null);
  const [nextPlayableMatch, setNextPlayableMatch] = useState({});
  const {t} = useTranslation();

  useEffect(() => {
    fetch(`https://localhost:8080/tournament/${tournamentid}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setTournament(data);
        var nextMatch = data.matchs.find(match => !match.winner && match.player1 && match.player2);
        if (!nextMatch)
          nextMatch = data.matchs.find(match => !match.winner && match.player1);
        setNextPlayableMatch(nextMatch);
      })
      .catch(error => {
        console.error('Error fetching tournament details:', error);
      });
  }, [tournamentid]);

  const renderMatches = () => {
    if (!tournament) return null;

    const { matchs, players, rounds } = tournament;

    matchs.sort((a, b) => a.id - b.id);

    const renderedMatches = [];

    for (let i = 1; i <= rounds; i++) {
      renderedMatches.push([]);
    }

    matchs.forEach(match => {
      const player1 = match.player1 ? players.find(player => player.id === match.player1.id) : null;
      const player2 = match.player2 ? players.find(player => player.id === match.player2.id) : null;
      const winner = match.winner ? players.find(player => player.id === match.winner.id) : null;
  
      let loser = null;
      let winnerStyle = {};
      let loserStyle = {};
  
      if (winner) {
        loser = winner.id === match.player1?.id ? player2 : player1;
  
        winnerStyle = {
          backgroundColor: 'lightgreen',
        };
  
        loserStyle = {
          backgroundColor: 'lightgray',
        };
      }
  
      const player1Style = winner && player1 ? winner.id === player1.id ? winnerStyle : loserStyle : {};
      const player2Style = winner && player2 ? winner.id === player2.id ? winnerStyle : loserStyle : {};
  
      const player1Name = player1 ? player1.name : 'TBD';
      const player2Name = player2 ? player2.name : 'TBD';
  
      const matchDisplay = (
        <div key={match.id} className="d-flex align-items-center mb-3">
          <div className="border rounded p-3 mr-3" style={player1Style}>
            <p>{player1Name}</p>
          </div>
          <div className="border rounded p-3" style={player2Style}>
            <p>{player2Name}</p>
          </div>
        </div>
      );
  
      renderedMatches[match.round - 1].push(matchDisplay);
    });
  
    const columns = renderedMatches.map((matches, index) => (
      <div key={index} className="col">
        {matches}
      </div>
    ));
  
    return (
      <div className="container-fluid">
        <div className="row">{columns}</div>
      </div>
    );
  };


  if (!tournament) {
    return <div>Invalid tournament</div>;
  }

  let terminate = (object) => {
    setTimeout(() => {
      fetch(`https://localhost:8080/tournament/${tournamentid}/play-next-match`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Origin': 'https://localhost:4000',
          },
          body: JSON.stringify({ nextMatchId: nextPlayableMatch.id, winnerId: object.winner }),
        })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            window.location.reload();
          })
          .catch(error => {
            console.error('Error while processing the next match:', error);
          });
    }, 1000);
  }
  
  return (
    <div className="container-fluid">
      <h1>{t('tournament_details')}</h1>
      <p>{t('tournament_name')}: {tournament.name}</p>
      <div className="row">
        <div className="col">
          {renderMatches()}
        </div>
      </div>
      <div className="d-flex justify-content-center  align-items-center h-100">
            <div>
              {nextPlayableMatch && (<KeyboardControls
                    map={[
                    { name: "Down01", keys: ['KeyS', 'KeyD'] },
                    { name: "Up01", keys: ['KeyW', 'KeyA'] },
                    { name: "Up02", keys: ['ArrowUp', 'ArrowLeft'] },
                    { name: "Down02", keys: ['ArrowDown', 'ArrowRight'] },
                    { name: "Serve", keys: ['Space'] },
                    ]}
                >
                <Canvas shadows linear flat camera={{ position: [0, 35, 0], fov: 40 }}>
                    <Game points={3} speed={3} terminate={terminate}></Game>
                </Canvas>
                </KeyboardControls>)}

            </div>
      </div>
    </div>
  );
}

export default TournamentBracket;
