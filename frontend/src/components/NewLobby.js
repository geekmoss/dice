import React from 'react';
import {Form, Modal, InputNumber, Button, Slider, Input} from "antd";
import {formItemTwoLinesLayout} from "./formTwoLines";


export default function NewLobby(props) {
    const { visible, onClose, onSubmit } = props;
    const [ points, setPoints ] = React.useState(10000);
    const [ password, setPassword ] = React.useState('');

    const onChange = (value) => {
        setPoints(value);
    }

    const onChangePassword = (value) => {
        setPassword(value);
    }

    return (
        <>
            <Form
                onFinish={(values) => {console.log(values); onSubmit(values);}}
                initialValues={{
                    points: points
                }}
                id={"newLobby"}
            >
                <Modal
                    title={"New lobby"}
                    visible={visible}
                    footer={[
                        <Button type={"primary"} htmlType={"submit"} key={"submit"} form={"newLobby"} >Create</Button>
                    ]}
                    onCancel={() => {onClose();}}
                >
                    <Form.Item
                        name={"passwd"}
                        label={"Password"}
                        {...formItemTwoLinesLayout}
                    >
                        <Input.Password
                            onChange={(val) => {onChangePassword(val);}}
                        />
                    </Form.Item>
                    <Form.Item
                        name={"points"}
                        label={"Points to win"}
                        {...formItemTwoLinesLayout}
                    >
                        <Slider
                            min={5000}
                            max={50000}
                            step={1000}
                            marks={{5000: '5000', 10000: '10000', 25000: '25000', 50000: '50000'}}
                            onChange={(val) => {onChange(val);}}
                            value={points}
                        />
                    </Form.Item>
                </Modal>
            </Form>
        </>
    );
}