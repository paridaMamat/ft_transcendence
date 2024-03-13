import React, { useState, useEffect } from 'react';
import Block from "../../components/block/Block";
import { useTranslation } from 'react-i18next';

function TournamentLocal() {
  const [numberOfPlayers, setNumberOfPlayers] = useState(2);
  const [tournamentName, setTournamentName] = useState('');
  const {t} = useTranslation();

  const [playerNames, setPlayerNames] = useState([]);

  useEffect(() => {
    setPlayerNames(Array(numberOfPlayers).fill(''));
  }, [numberOfPlayers]);

  const [errorMessage, setErrorMessage] = useState('');

  const handlePlayerNameChange = (index, newName) => {
    const updatedPlayers = [...playerNames];
    updatedPlayers[index] = newName;
    setPlayerNames(updatedPlayers);
    checkForDuplicates(updatedPlayers);
  };

  const checkForDuplicates = (names) => {
    const uniqueNames = new Set(names.filter(name => name.trim() !== ''));
    if (uniqueNames.size !== names.filter(name => name.trim() !== '').length) {
      setErrorMessage('Duplicate player names are not allowed.');
    } else {
      setErrorMessage('');
    }
  };

  const handleStartTournament = async () => {
    if (errorMessage) {
      alert(errorMessage);
      return;
    }

    try {
      const response = await fetch('https://localhost:8080/tournament/create_local_tournament/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Origin': 'https://localhost:4000',
        },
        body: JSON.stringify({
          name: tournamentName,
          numberOfPlayers: numberOfPlayers,
          playerNames: playerNames.filter(name => name.trim() !== '')
        })
      });
  
      if (response.ok) {
        const data = await response.json();
        window.location.href = `/tournament/${data.tournament_id}`;
      } else {
        throw new Error('Erreur lors de la création du tournoi');
      }
    } catch (error) {
      console.error('Erreur lors de la création du tournoi:', error);
    }
  };

  return (
        <Block title={t('tournament_setup')}>
          <div className="text-center">
            <label>{t('tournament_name')} :
              <input
                className="form-control"
                type="text"
                placeholder="Enter tournament name"
                value={tournamentName}
                onChange={(e) => setTournamentName(e.target.value)}
              />
            </label>
            <label>{t('tournament_players')} :
              <input
                className="form-control"
                type="number"
                min={2}
                max={8}
                value={numberOfPlayers}
                onChange={(e) => setNumberOfPlayers(e.target.value)}
              />
            </label>
            {Array.from({ length: numberOfPlayers }).map((_, index) => (
              <input
                className="form-control"
                key={index}
                type="text"
                placeholder={`Player ${index + 1} name`}
                value={playerNames[index] || ''}
                onChange={(e) => handlePlayerNameChange(index, e.target.value)}
              />
            ))}
            {errorMessage && <p className="text-danger">{errorMessage}</p>}
            <button type="button" className="btn btn-info" onClick={handleStartTournament}>{t('tournament_start')}</button>
          </div>
        </Block>
  );
}

export default TournamentLocal;
