import React from 'react';
import Game from "./pages/Game";
import Lobbies from "./pages/Lobbies";
import UsernamePrompt from "./components/UsernamePrompt";
import { HashRouter as Router, Route } from "react-router-dom";
import 'antd/dist/antd.dark.min.css';

function App() {


    return (
        <div
            className="App"
            style={{
                padding: "16px 128px"
            }}
        >
            <Router>
                <Route path="/" exact component={Lobbies} />
                <Route path="/game/:key" component={Game} />

                <UsernamePrompt />
            </Router>
        </div>
    );
}

export default App;
