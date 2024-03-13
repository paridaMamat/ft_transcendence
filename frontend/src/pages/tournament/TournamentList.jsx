import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Block from "../../components/block/Block";
import { useTranslation } from 'react-i18next';

function TournamentList() {
  const [tournaments, setTournaments] = useState([]);
  const {t} = useTranslation();

  useEffect(() => {
    fetch('https://localhost:8080/tournament/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setTournaments(data);
      })
      .catch(error => {
        console.error('Error fetching tournaments:', error);
      });
  }, []);

  return (
    <Block title={t("tournament_list")}>
      <div className="list-group">
        {tournaments.map(tournament => (
          <Link
            to={`/tournament/${tournament.id}`}
            className="list-group-item list-group-item-action"
            key={tournament.id}
          >
            <div className="d-flex w-100 justify-content-between">
              <h5 className="mb-1">{tournament.name}</h5>
              <small className="text-body-secondary">Round : {tournament.current_round} / {tournament.rounds}</small>
            </div>
            <small className="text-body-secondary">
              {tournament.players.length}/8 {tournament.online ? 'online' : 'local'}
            </small>
          </Link>
        ))}
      </div>
    </Block>
  );
}

export default TournamentList;

