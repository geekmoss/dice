import React from 'react';
import getUsername from "../utils/user";
import {Socket} from "../utils/websocket";
import {Row, Col, Space, notification, Divider, Button, Modal} from "antd";
import {Link} from "react-router-dom";
import PlayerGameBoard from "../components/PlayerGameBoard";
import { TrophyTwoTone } from "@ant-design/icons";
import WinnerModal from "../components/WinnerModal";


const gameNotFound = <div><h2>Game not found</h2>
    <Link to={"/"}>Back to lobbies</Link></div>

const getQueryParam = (query) => {
    if (query.substr(0, 1) === "?") {
        query = query.substr(1);
    }

    let params = {};
    query.split("&").map((v) => {
        const [key, value] = v.split("=");
        params[key] = value;
        return key;
    });

    return params;
}


export default class Game extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            game_not_found: false,
            needs_password: null,
            player1: {},
            player2: {},
            winner: null,
        };

        this.key = props.match.params.key;
        this.password = getQueryParam(props.location.search).password;
        this.history = props.history;
        this.socket = undefined;
    }

    componentDidMount() {
        this.socket = new Socket(`game/${this.key}`, {
            game_not_found: () => {
                this.setState({game_not_found: true});
            },
            game_status: (data, socket) => {
                console.log(data);
                this.setState({
                    player1: data.player1,
                    player2: data.player2,
                    needs_password: data.needs_password,
                    you_are: data.you_are,
                });
            },
            join_result: (data, socket) => {
                console.log(data);
                this.setState({you_are: data.you_are});
                if (!data.result) {
                    notification.error({
                        message: 'Take Seat',
                        description: 'Wrong password or this seat isn\'t yours'
                    });
                }
            },
            winner: (data, socket) => {

            }
        }, (socket) => {
            socket.sendMessage({
                event: "game_status"
            })
        });
    }

    handleTakeSeat() {
        let password = null;
        if (this.state.needs_password) {
            password = this.password ? this.password : prompt("Enter game password");
        }

        this.socket.sendMessage({
            event: "join",
            player_name: getUsername(),
            password: password,
        })
    }

    handleComboClick(c) {
        this.socket.sendMessage({
            event: "combo_click",
            combo: c,
        });
    }

    handleTriggerEvent(event) {
        this.socket.sendMessage({event});
    }

    isUsable(action) {
        const isPlayer = this.state.you_are > 0;
        if (!isPlayer)
            return false;

        const player = this.state[`player${this.state.you_are}`]
        console.log(player.state);

        return ({
            roll: () => (player.state === 1),
            endTurn: () => (player.state === 1),
            confirmPick: () => ((player.state === 2) && player.picked_dice.length > 0),
            resetPick: () => ((player.state === 2) && player.picked_dice.length > 0),
            pickCombo: () => ((player.state === 2) && player.combos.lenght > 0),
        })[action]();
    }

    render() {
        if (this.state.game_not_found) {
            return gameNotFound;
        }

        return (
            <>
                <Row>
                    <Col span={12}>
                        <PlayerGameBoard
                            player={this.state.player1}
                            canTryTakeSeat={!this.state.player1.joined && (this.state.you_are === 0)}
                            onTakeSeat={() => {this.handleTakeSeat();}}
                            onComboClick={(c) => {
                                if (this.state.you_are === 1 ) {
                                    this.handleComboClick(c);
                                }
                            }}
                        />
                    </Col>
                    <Col span={12}>
                        <PlayerGameBoard
                            player={this.state.player2}
                            canTryTakeSeat={!this.state.player2.joined && (this.state.you_are === 0)}
                            onTakeSeat={() => {this.handleTakeSeat();}}
                            onComboClick={(c) => {
                                if (this.state.you_are === 2 ) {
                                    this.handleComboClick(c);
                                }
                            }}
                        />
                    </Col>
                </Row>
                <div style={this.state.you_are > 0 ? {} : {display: 'none'}}>
                    <Divider />
                    <Space>
                        <Button
                            onClick={() => {this.handleTriggerEvent('roll');}}
                            disabled={!this.isUsable('roll')}
                        >
                            Roll
                        </Button>

                        <Button
                            onClick={() => {this.handleTriggerEvent('end_turn');}}
                            disabled={!this.isUsable('endTurn')}
                        >
                            End Turn
                        </Button>

                        <Button
                            onClick={() => {this.handleTriggerEvent('confirm_pick');}}
                            disabled={!this.isUsable('confirmPick')}
                        >
                            Confirm Pick
                        </Button>

                        <Button
                            danger onClick={() => {this.handleTriggerEvent('reset_pick');}}
                            disabled={!this.isUsable('resetPick')}
                        >
                            Reset Pick
                        </Button>
                    </Space>
                </div>

                <WinnerModal visible={this.state.winner !== null} player={this.state[`player${this.state.winner}`]} />
            </>
        );
    }
}