export class Socket {
    constructor(endpoint, events, onopen) {
        this.socket = new WebSocket(`ws://localhost:8000/ws/${endpoint}`);
        this._connected = false;

        this.socket.onopen = () => {
            console.log("Websocket opened.");

            this._connected = true;
            if (onopen !== undefined) {
                onopen(this);
            }
        }

        this.socket.onmessage = (msg) => {
            try {
                const json = JSON.parse(msg.data);
                events[json.event](json, this);
            } catch (e) {
                console.warn(e, msg);
            }
        }

        this.socket.onclose = () => {
            console.log("Websocket closed.");
            this._connected = false;
        }
    }

    sendMessage(json) {
        this.socket.send(JSON.stringify(json));
    }

    isConnected() {
        return this._connected;
    }
}
