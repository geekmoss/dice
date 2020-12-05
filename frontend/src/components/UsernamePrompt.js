import React from 'react';
import { Modal, Input, Button } from 'antd';
import {isUsernameSet, setUsername} from '../utils/user.js'


class UsernamePrompt extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            showPrompt: false,
            inputUsername: ""
        }
    }

    componentDidMount() {
        if (!isUsernameSet()) {
            this.setState({showPrompt: true});
        }
    }

    handleChange(e) {
        const { value } = e.target;
        this.setState({inputUsername: value});
    }

    handleOk() {
        if (this.state.inputUsername.trim().length > 0) {
            setUsername(this.state.inputUsername);
            this.setState({
                showPrompt: false
            });
        }
    }

    render() {
        return (
            <>
                <Modal
                    closable={false}
                    visible={this.state.showPrompt}
                    title={"Please enter your username"}
                    onOk={() => {this.handleOk();}}
                    footer={[
                        <Button key={"ok"} type={"primary"} onClick={() => {this.handleOk();}}>Set username</Button>
                    ]}
                >
                    <Input
                        placeholder="Username"
                        onChange={(e) => {this.handleChange(e);}}
                        onPressEnter={() => {this.handleOk();}}
                    />
                </Modal>
            </>
        );
    }
}

export default UsernamePrompt;