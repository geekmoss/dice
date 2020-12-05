import React from 'react';
import { Socket } from "../utils/websocket";
import NewLobby from "../components/NewLobby";
import {Button, message} from "antd";
import getUsername from "../utils/user";
import LobbyList from "../components/LobbyList";


export default class Lobbies extends React.Component {
    constructor(props) {
        super(props);

        this.history = props.history;

        this.state = {
            showNewLobby: false,
            lobbies: []
        }
    }

    componentDidMount() {
        this.socket = new Socket("list", {
            list: (data, socket) => {
                this.setState({lobbies: data.lobbies});
            },
            new_room: (data, socket) => {
                console.log(data);
                this.history.push(`/game/${data.room.key}?password=${data.room.password}`);
            }
        }, (socket) => {
            socket.sendMessage({event: "list"});
        });
    }

    handleSubmitNewLobby(values) {
        console.log(values);

        const username = getUsername();
        this.socket.sendMessage({
            event: "new_room",
            room: {
                player_name: username,
                password: values.passwd,
                points: values.points
            }
        });
    }

    handleCloseNewLobby() {
        this.setState({showNewLobby: false});
    }

    handleOpenNewLobby() {
        if (!this.socket.isConnected()) {
            message.warn("Cannot create new lobby, try reload page.", 10);
            return;
        }
        this.setState({showNewLobby: true});
    }

    render() {
        return (
            <>
                <h1>Lobbies of Dice</h1>

                <LobbyList lobbies={this.state.lobbies} newLobbyButton={
                    <Button onClick={() => {this.handleOpenNewLobby();}}>New lobby</Button>
                } />

                <NewLobby
                    visible={this.state.showNewLobby}
                    onClose={() => {this.handleCloseNewLobby();}}
                    onSubmit={(values) => {this.handleSubmitNewLobby(values);}}
                />
            </>
        );
    }

}