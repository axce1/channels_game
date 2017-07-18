import React from 'react';
import ReactDOM from 'react-dom';
import Websocket from 'react-websocket'
import $ from 'jquery'

import PlayerGames from './PlayerGames'
 
class LobbyBase extends React.Component {
 
    constructor(props) {
        super(props);
        this.state = {
            player_game_list: [],
            available_game_list: []
        }
 
        this.sendSocketMessage = this.sendSocketMessage.bind(this);
    }

    getPlayerGames() {
        this.severRequest = $.get('http://localhost:8000/player-games/?format=json', function(result) {
            this.setState({
                player_game_list: result,
            })
        }.bind(this))
    }
 
    componentDidMount() {
        this.getPlayerGames()
    }
 
    componentWillUnmount() {
        this.serverRequest.abort();
    }
 
    handleData(data) {
        let result = JSON.parse(data)
        this.getPlayerGames()
        this.setState({available_game_list: result})
    }
 
    sendSocketMessage(message){
       const socket = this.refs.socket
       socket.state.ws.send(JSON.stringify(message))
    }
 
    render() {
        return (
 
            <div className="row">
                <Websocket ref="socket" url={this.props.socket}
                    onMessage={this.handleData.bind(this)} reconnect={true}/>
                <div className="col-lg-4">
                    <PlayerGames player={this.props.current_user} game_list={this.state.player_game_list}
                            sendSocketMessage={this.sendSocketMessage} />
                </div>
            </div> 
        )
    }
}
 
LobbyBase.propTypes = {
    socket: React.PropTypes.string
};
 
export default LobbyBase;
