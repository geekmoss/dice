export class Socket {
    constructor(endpoint, events, onopen) {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const host = window.location.hostname !== "localhost" ? window.location.host : 'localhost:8000'

        this.socket = new WebSocket(`${protocol}://${host}/ws/${endpoint}`);
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
