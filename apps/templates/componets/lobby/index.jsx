import React from 'react';
import LobbyBase from './LobbyBase.jsx'
import ReactDOM from 'react-dom'
import $ from 'jquery'
 
var lobby_sock = 'ws://' + window.location.host + "/lobby/"
var current_user = null
 
function render_component(){
    ReactDOM.render(<LobbyBase current_user={current_user} socket={lobby_sock}/>, document.getElementById('lobby_component'))
}
 
render_component()
