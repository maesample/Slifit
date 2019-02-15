import React from 'react'
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { hot } from 'react-hot-loader'

import App from "./App";
import HomePage from './containers/HomePage';

class AppRouter extends React.Component {
    render() {
        return (
        <Router>
            <App>
                <Switch>
                    <Route path="/" component={HomePage}/>
                </Switch>
            </App>
        </Router>
        )
    }
}

export default hot(module)(AppRouter)