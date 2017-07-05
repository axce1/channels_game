import React from 'react'

class PrayerGames extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            game_list: this.props.game_list
        }
    }

    this.onCreateGameClick = this.onCreateGameClick.bind(this)
    this.renderButton = this.renderButton.bind(this)
    this.renderOpponent = this.renderOpponent.bind(this)
    }
    
    onCreateGameClick(event) {
        this.props.sendSocketMessage({action: "create_game"})
    }
