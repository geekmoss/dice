import React from 'react';
import { Table } from "antd";
import { LockOutlined } from "@ant-design/icons";
import { Link } from "react-router-dom";

export default function LobbyList({ lobbies, newLobbyButton }) {
    return (
        <>
            <Table
                dataSource={lobbies}
                columns={[
                    {
                        title: 'Lobby type',
                        key: 'type',
                        render: (text, record) => {
                            return (record.has_password ? (<><LockOutlined /> Private</>)  : 'Public');
                        },
                        filters: [
                            {
                                text: 'Public',
                                value: false
                            },
                            {
                                text: 'Private',
                                value: true
                            }
                        ],
                        onFilter: (value, record) => {
                            console.log(value, record);
                            return record.has_password === value
                        }
                    },
                    {
                        title: 'State',
                        key: 'state',
                        render: (text, record) => {
                            if (record.player_2_points + record.player_1_points > 0 || record.player_2_name !== null) {
                                return "Game in progress";
                            }
                            else {
                                return "Waiting for opponent";
                            }
                        },
                        filters: [
                            {
                                text: 'Waiting for opponents',
                                value: false
                            },
                            {
                                text: 'In game',
                                value: true
                            }
                        ],
                        onFilter: (value, record) => ((record.player_2_points + record.player_1_points > 0 || record.player_2_name !== null) === value)
                    },
                    {
                        title: 'Player 1',
                        key: 'player',
                        render: (text, record) => (<>
                                <strong>{record.player_1_name}</strong> with {record.player_1_points} points
                            </>)
                    },
                    {
                        title: 'Player 2',
                        key: 'player',
                        render: (text, record) => (record.player_2_name === null ? '-' :
                            <>
                                <strong>{record.player_2_name}</strong> with {record.player_2_points} points
                            </>)
                    },
                    {
                        title: 'Points to win',
                        dataIndex: 'points_to_win',
                        key:'toWin'
                    },
                    {
                        title: newLobbyButton,
                        key: 'join',
                        render: (text, record) => {
                            return <Link to={`/game/${record.key}`}>Join</Link>
                        }
                    }
                ]}
            />
        </>
    );
}