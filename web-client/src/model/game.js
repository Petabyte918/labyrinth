import Vue from "vue";
import MazeCard from "@/model/mazeCard.js";
import Player from "@/model/player.js";
import Graph from "@/model/mazeAlgorithm.js";
import ValueError from "@/util/exceptions";

export const MOVE_ACTION = "MOVE";
export const SHIFT_ACTION = "SHIFT";
export const NO_ACTION = "NONE";

export default class Game {
    constructor() {
        this.n = 7;
        this.mazeCards = [];
        this.leftoverMazeCard = {};
        this._players = [];
        this.nextAction = { playerId: 0, action: NO_ACTION };
        this.isLoading = false;
        this.disabledInsertLocation = null;
    }

    mazeCardsAsList() {
        return [].concat.apply([], this.mazeCards);
    }

    mazeCardById(id) {
        for (var row = 0; row < this.mazeCards.length; row++) {
            for (var col = 0; col < this.mazeCards[row].length; col++) {
                if (this.mazeCards[row][col].id == id) {
                    return this.mazeCards[row][col];
                }
            }
        }
        if (this.leftoverMazeCard.id == id) {
            return this.leftoverMazeCard;
        }
        return null;
    }

    getMazeCard(location) {
        if (this.isInside(location)) {
            return this.mazeCards[location.row][location.column];
        } else {
            throw new RangeError();
        }
    }

    setMazeCard(location, mazeCard) {
        if (this.isInside(location)) {
            this.mazeCards[location.row][location.column] = mazeCard;
        } else {
            throw new RangeError();
        }
    }

    shift(location) {
        if (this._locationsEqual(location, this.disabledInsertLocation)) {
            throw new ValueError();
        }

        if (!this.isInside(location)) {
            throw new RangeError();
        }
        var shiftLocations = [];
        let opposite_location = null;
        if (location.row === 0) {
            shiftLocations = this._columnLocations(location.column);
            opposite_location = { row: this.n - 1, column: location.column };
        } else if (location.row === this.n - 1) {
            shiftLocations = this._columnLocations(location.column);
            shiftLocations.reverse();
            opposite_location = { row: 0, column: location.column };
        } else if (location.column === this.n - 1) {
            shiftLocations = this._rowLocations(location.row);
            shiftLocations.reverse();
            opposite_location = { row: location.row, column: 0 };
        } else if (location.column === 0) {
            shiftLocations = this._rowLocations(location.row);
            opposite_location = { row: location.row, column: this.n - 1 };
        }
        if (shiftLocations.length === this.n) {
            this._shiftAlongLocations(shiftLocations);
            this.disabledInsertLocation = opposite_location;
        } else {
            throw new ValueError();
        }
    }

    _locationsEqual(locA, locB) {
        return locA && locB && locA.row === locB.row && locA.column === locB.column;
    }

    hasPlayer(playerId) {
        for (let player of this._players) {
            if (player.id === playerId) {
                return true;
            }
        }
        return false;
    }

    getPlayer(playerId) {
        for (let player of this._players) {
            if (player.id === playerId) {
                return player;
            }
        }
        throw new ValueError();
    }

    addPlayer(player) {
        if (!this.hasPlayer(player.id)) {
            this._players.push(player);
        }
    }

    getComputerPlayers() {
        let result = [];
        for (var player of this._players) {
            if (player.isComputer) {
                result.push(player);
            }
        }
        return result;
    }

    getPlayers() {
        return this._players;
    }

    deletePlayerById(playerId) {
        let position = -1;
        for (var index = 0; index < this._players.length; index++) {
            if (this._players[index].id === playerId) {
                position = index;
            }
        }
        if (position > 0) {
            this._players.splice(position, 1);
        }
    }

    move(playerId, targetLocation) {
        var player = this.getPlayer(playerId);
        var targetMazeCard = this.getMazeCard(targetLocation);
        var sourceMazeCard = player.mazeCard;
        sourceMazeCard.removePlayer(player);
        targetMazeCard.addPlayer(player);
        player.mazeCard = targetMazeCard;
    }

    isMoveValid(playerId, targetLocation) {
        if (this.nextAction.playerId !== playerId) {
            return false;
        }
        if (this.nextAction.action !== MOVE_ACTION) {
            return false;
        }
        let player = this.getPlayer(playerId);
        let sourceLocation = player.mazeCard.location;
        return new Graph(this).isReachable(sourceLocation, targetLocation);
    }

    _columnLocations(column) {
        var locations = [];
        for (let row = 0; row < this.n; row++) {
            locations.push({ row: row, column: column });
        }
        return locations;
    }

    _rowLocations(row) {
        var locations = [];
        for (let column = 0; column < this.n; column++) {
            locations.push({ row: row, column: column });
        }
        return locations;
    }

    _shiftAlongLocations(locations) {
        var pushedCard = this.leftoverMazeCard;
        this.leftoverMazeCard = this.getMazeCard(locations[this.n - 1]);
        this.leftoverMazeCard.setLeftoverLocation();
        for (let i = this.n - 1; i > 0; i--) {
            this.setMazeCard(locations[i], this.getMazeCard(locations[i - 1]));
            this.getMazeCard(locations[i]).setLocation(locations[i]);
        }
        this._transferPlayers(this.leftoverMazeCard, pushedCard);
        var first = locations[0];
        pushedCard.setLocation(first);
        Vue.set(this.mazeCards[first.row], first.column, pushedCard);
    }

    _transferPlayers(sourceMazeCard, targetMazeCard) {
        while (sourceMazeCard.players.length) {
            var player = sourceMazeCard.players.pop();
            player.mazeCard = targetMazeCard;
            targetMazeCard.addPlayer(player);
        }
    }

    createFromApi(apiState, userId = 0) {
        this.isLoading = true;
        var apiMazeCards = apiState.mazeCards;
        this._sortApiMazeCards(apiMazeCards);
        if (this.leftoverMazeCard.id != apiMazeCards[0].id) {
            this.leftoverMazeCard = MazeCard.createFromApi(apiMazeCards[0]);
        }

        this._mazeCardsFromSortedApi(apiMazeCards);
        this._playersFromApi(apiState, userId);

        let objectiveCard = this.mazeCardById(apiState.objectiveMazeCardId);
        objectiveCard.hasObject = true;

        if (apiState.nextAction) {
            this.setNextAction(apiState.nextAction.playerId, apiState.nextAction.action);
        }

        this.disabledInsertLocation = this._findMissingInsertLocation(
            apiState.enabledShiftLocations
        );

        this.isLoading = false;
    }

    _playersFromApi(apiState, userId) {
        let remainingColors = [3, 2, 1, 0];
        let toRemove = new Set(this._players.map(player => player.id));
        apiState.players.sort(function(p1, p2) {
            return p1.id - p2.id;
        });
        for (let index = 0; index < apiState.players.length; index++) {
            let apiPlayer = apiState.players[index];
            let playerCard = this.mazeCardById(apiPlayer.mazeCardId);
            let player;
            if (this.hasPlayer(apiPlayer.id)) {
                player = this.getPlayer(apiPlayer.id);
                player.colorIndex = remainingColors.pop();
            } else {
                player = Player.newFromApi(apiPlayer, remainingColors.pop());
                if (userId === player.id) {
                    player.isUser = true;
                }
            }
            player.mazeCard = playerCard;
            playerCard.addPlayer(player);
            toRemove.delete(player.id);
            if (!this.hasPlayer(player.id)) {
                this.addPlayer(player);
            }
        }
        for (let id of toRemove) {
            this.deletePlayerById(id);
        }
    }

    _findMissingInsertLocation(apiInsertLocations) {
        let enabledInsertLocations = new Set();
        for (let location of apiInsertLocations) {
            enabledInsertLocations.add(this._key(location));
        }
        let allInsertLocations = [];
        for (let position = 1; position < this.n - 1; position += 2) {
            allInsertLocations.push({ row: 0, column: position });
            allInsertLocations.push({ row: position, column: 0 });
            allInsertLocations.push({ row: this.n - 1, column: position });
            allInsertLocations.push({ row: position, column: this.n - 1 });
        }
        for (let location of allInsertLocations) {
            if (!enabledInsertLocations.has(this._key(location))) {
                return location;
            }
        }
        return null;
    }

    _key(location) {
        return location.row * this.n + location.column;
    }

    _addInsertLocation(locationsMap, location) {
        locationsMap.set(location.row * this.n + location.column, location);
    }

    setNextAction(playerId, action) {
        this.nextAction.playerId = playerId;
        this.nextAction.action = action;
        this.getPlayer(playerId).turnAction = action;
    }

    _sortApiMazeCards(apiMazeCards) {
        apiMazeCards.forEach(card => {
            if (card.location === null) {
                card.location = {
                    row: -1,
                    column: -1
                };
            }
        });
        apiMazeCards.sort((card1, card2) =>
            this._compareApiLocations(card1.location, card2.location)
        );
    }

    _compareApiLocations(location1, location2) {
        if (location1.row == location2.row) {
            return location1.column - location2.column;
        }
        return location1.row - location2.row;
    }

    _mazeCardsFromSortedApi(sortedApiMazeCards) {
        this.mazeCards.splice(0, this.n);
        var index = 1;
        for (var row = 0; row < this.n; row++) {
            this.mazeCards.push([]);
            for (var col = 0; col < this.n; col++) {
                this.mazeCards[row].push(MazeCard.createFromApi(sortedApiMazeCards[index]));
                index++;
            }
        }
    }

    isInside(location) {
        return (
            location.row >= 0 &&
            location.row < this.n &&
            location.column >= 0 &&
            location.column < this.n
        );
    }
}
