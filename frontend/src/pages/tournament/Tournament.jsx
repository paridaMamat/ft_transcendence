import React, { useState } from 'react';
import Block from "../../components/block/Block";
import Button from "../../components/button/Button";

function Tournament() {
    const url = "s://localhost:8080/tournament/create_tournament/";
    const [lobbyName, setLobbyName] = useState('');
    const [createdLobby, setCreatedLobby] = useState(null);

    const handleCreateLobby = async () => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Origin': 'https://localhost:4000',
                },
                body: JSON.stringify({ name: lobbyName }),
            });

            if (response.ok) {
                const data = await response.json();
                setCreatedLobby(data);
            } else {
                throw new Error('Erreur lors de la création du lobby');
            }
        } catch (error) {
            console.error('Erreur lors de la création du lobby :', error);
        }
    };

    return (
        <Block title="Create Tournament Lobby">
            <div className="text-center">
                <input
                    className="form-control"
                    type="text"
                    placeholder="Nom du lobby"
                    value={lobbyName}
                    onChange={(e) => setLobbyName(e.target.value)}
                />
                <button type="button" className="btn btn-info" onClick={handleCreateLobby}>
                    Créer le lobby
                </button>
                {createdLobby && (
                    <p className="mt-3">Lobby créé : {createdLobby.name}</p>
                )}
            </div>
        </Block>
    )
}

export default Tournament;
