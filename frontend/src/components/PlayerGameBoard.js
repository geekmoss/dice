import React from 'react';
import {Space, Button, Row, Col, Divider, List, Badge} from "antd";
import Dice from "./Dice";


const STATES = {
    0: {
        title: 'End of game'
    },
    1: {
        title: "On Turn, Can roll",
    },
    2: {
        title: "On Turn, Picking dice",
    },
    3: {
        title: "End of Turn or No possible option"
    }
}


export default function PlayerGameBoard({player, canTryTakeSeat, onTakeSeat, onComboClick}) {
    const {
        joined,
        name,
        picked_points,
        points,
        points_progress,
        state,
        dice,
        active_dice,
        picked_dice,
        stored_dice,
        combos,
    } = player;

    if (joined === undefined) {
        return '';
    }

    return (
        <>
            <Row>
                <Col span={12}>
                    <h1>
                        <Space>
                            <Badge status={!joined && name ? "red" : "success"} />
                            {name ? name : '---'}
                        </Space>
                    </h1>
                </Col>
                <Col span={12}>
                    {!canTryTakeSeat ? '' :
                        <Button onClick={onTakeSeat}>Take seat</Button>}
                </Col>
            </Row>
            <h2>{STATES[state].title}</h2>
            <h4><pre>{points} points</pre></h4>

            <Divider />
            <Row>
                <Col span={12}>
                    <h2>Active dice</h2>
                    <Space>
                        {active_dice ? active_dice.map((d, i) => {
                            return <Dice
                                    value={d}
                                    key={i}
                                />
                        }) : ''}
                    </Space>

                    <h2>Picked dice</h2>
                    <Space>
                        {picked_dice ? picked_dice.map((d, i) => {
                            return <Dice
                                    value={d}
                                    key={i}
                                />
                        }) : ''}
                    </Space>

                    <h2>Stored dice</h2>
                    <Space>
                        {stored_dice ? stored_dice.map((d, i) => {
                            return <Dice
                                    value={d}
                                    key={i}
                                />
                        }) : ''}
                    </Space>

                    <h6>Possible take {picked_points} points</h6>
                </Col>
                <Col span={12}>
                    <h3>Combinations</h3>
                    <List
                        itemLayout={"horizonzal"}
                        dataSource={combos}
                        renderItem={item => {
                            return <List.Item
                                actions={[
                                    <Button size={"xs"} type={"text"} onClick={() => {onComboClick(item);}}>Pick</Button>
                                ]}

                            >
                                <List.Item.Meta
                                    title={<Space>
                                        {item.indexes.map((i) => (<Dice
                                            value={dice[i]}
                                            key={i}
                                        />))}
                                    </Space>}
                                    description={<em>Points: {item.points}</em>} />
                            </List.Item>
                        }}
                    >


                    </List>
                </Col>
            </Row>
        </>
    );
}