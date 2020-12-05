import React from 'react';
import {Button, Modal} from "antd";
import {TrophyTwoTone} from "@ant-design/icons";


export default function WinnerModal({visible, player}) {
    if (player === undefined) {
        player = {};
    }
    return (
        <>
            <Modal
                visible={visible}
                title={"Winner!"}
                footer={[
                    <Button type="primary" key="ok" onClick={() => {this.history.push('/');}}>Ok</Button>
                ]}
            >
                <TrophyTwoTone /> {player.name} is winner!
            </Modal>
        </>
    );
}