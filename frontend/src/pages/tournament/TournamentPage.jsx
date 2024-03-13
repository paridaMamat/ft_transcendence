import React from 'react';

import Tournament from './Tournament';
import TournamentList from './TournamentList';
import TournamentLocal from './TournamentLocal';
import { useTranslation } from 'react-i18next';

function TournamentPage() {
  const {t} = useTranslation();
  return (
    <div className="tournament-page">
		<div className="container-fluid">
      		<div className="row">
      			<h1>{t('tournament_page')}</h1>
	  			<Tournament /> {}
        		<TournamentList /> {}
				<TournamentLocal /> {}
			</div>
		</div>
    </div>
  );
}

export default TournamentPage;