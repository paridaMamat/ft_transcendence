import i18next from "i18next";
import { director } from "../../lib/Director";
import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import "./Users.css";
import { useParams } from "react-router-dom";

const Match = ({ username }) => {
    const [userMatches, setUserMatches] = useState([]);

    useEffect(() => {
        let getMatchs = async() => {
            let data = await director("game/user-matches/" + username)
            setUserMatches(data);
        }
        getMatchs();
    }, []);


    return (
        <div>
            {userMatches.map(match => (
                <div key={match.id}>
                    <div className="changelog-item">
                        <div className="changelog-main">
                            <p className="title">
                                <span className="reason">Score : { match.score_player1} -  { match.score_player2}</span>
                            </p>
                            <p className="content">
                                <a href={`${match.player1}`}>{match.player1}</a> vs <a href="">{ match.player2 ? match.player2 : "anonyme" }</a> on { match.game_mode }
                            </p>
                            <span>{ new Intl.DateTimeFormat('fr-FR', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(new Date(match.date_played)) }</span>
                            </div>
                            <div className="changelog-middle"></div>
                            <div className="changelog-left">
                            </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

function User() {
	const { username } = useParams();
	const [user, setUser] = useState({});
	const {t} = useTranslation();

    useEffect(() => {
        let getUser = async() => {
            let data = await director("auth/get_user/" + username)
            setUser(data);
        }
        getUser();
    }, [])

    return (
        <>
            <div className="profile">
                <div className="container-fluid">
                <div className="user-header">
                </div>
                    <div className="row">
                        <div className="col-md-4 user-box ">
                            <div className="p-2 d-flex justify-content-between">
                                <span className="">{t('games_won')}</span>
                                <span className="">{user ? user.games_won : 0}</span>
                            </div>
                            <div className="p-2 d-flex justify-content-between">
                                <span className="">{t('games_lost')}</span>
                                <span className="">{user ? user.games_lost : 0}</span>
                            </div>
                            <div className="p-2 d-flex justify-content-between">
                                <span className="">{user.available ? "Available" : "Unavailable "}</span>
                            </div>
                        </div>
                        <div className="col-md-4"></div>
                        <div className="col-md-3">
                            <div className="bg-image-item profile-image rounded user-image" style={{ backgroundImage: "url(" + (user.profile_url ? "https://127.0.0.1:8080" + user.profile_url : "/marvin.png") + ")", margin: "5px"}}></div>
                        </div>
                    </div>
                </div>

            </div>
            <div className="changelogs-list my-3">
                <Match username={username}></Match>
            </div>
        </>
    )
}

export default User