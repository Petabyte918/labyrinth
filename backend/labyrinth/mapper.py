""" Mapper implementation, maps between Model objects and Data Transfer Objects (DTOs).

There are no specific classes for these DTOs,
instead they are data structures built of dictionaries and lists,
which in turn are automatically translatable to structured text (JSON or XML)
"""
from labyrinth.model import Game, Player, MazeCard, BoardLocation, Board
#from labyrinth.service import ApiException

_PLAYERS = "players"
_MAZE_CARDS = "mazeCards"
_ID = "id"
_MAZE_CARD_ID = "mazeCardId"
_DOORS = "doors"
_LOCATION = "location"
_ROTATION = "rotation"
_ROW = "row"
_COLUMN = "column"
_LEFTOVER_ROTATION = "leftoverRotation"
_KEY = "key"
_MESSAGE = "userMessage"


def game_to_dto(game: Game, player_id=None):
    """Maps a game to a DTO

    :param game: an instance of model.Game
    :param player_id: an identifier of a player.
                      If given, only returns the state from the view of the player.
    :return: a structure whose JSON representation is valid for the API
    """
    game_dto = dict()
    if player_id is None:
        game_dto[_PLAYERS] = [_player_to_dto(player) for player in game.players]
    else:
        game_dto[_PLAYERS] = [_player_to_dto(player) for player in game.players
                              if player.identifier is player_id]
    game_dto[_MAZE_CARDS] = []
    game_dto[_MAZE_CARDS].append(_maze_card_to_dto(game.leftover_card, None))
    for location in Board.board_locations():
        maze_card = game.board[location]
        game_dto[_MAZE_CARDS].append(_maze_card_to_dto(maze_card, location))
    return game_dto


def dto_to_game(game_dto):
    """ maps a DTO to a game

    :param game_dto: a dictionary representing the API structure of the game
    :return: a Game instance whose state is equal to the DTO
    """
    game = Game()
    maze_card_by_id = {}
    for maze_card_dto in game_dto[_MAZE_CARDS]:
        maze_card, board_location = _dto_to_maze_card(maze_card_dto)
        if board_location is None:
            game.leftover_card = maze_card
        else:
            game.board[board_location] = maze_card
        maze_card_by_id[maze_card.identifier] = maze_card
    game.players = [_dto_to_player(player_dto, maze_card_by_id)
                    for player_dto in game_dto[_PLAYERS]]
    return game


def dto_to_shift_action(shift_dto):
    """ Maps the DTO for the shift api method to the parameters of the model method
    :param shift_dto: a dictionary representing the body of the shift api method.
    Expected to be of the form
    {
        location: {
            row: <int>
            column: <int>
        },
        leftoverRotation: <int>
    }
    :return: a BoardLocation instance and an integer for the leftover maze card rotation
    """
    return _dto_to_board_location(shift_dto[_LOCATION]), shift_dto[_LEFTOVER_ROTATION]


def dto_to_move_action(move_dto):
    """ Maps the DTO for the move api method to the parameters of the model method
    :param move_dto: a dictionary representing the body of the move api method.
    Expected to be of the form
    {
        location: {
            row: <int>
            column: <int>
        }
    }
    :return: a BoardLocation instance
    """
    return _dto_to_board_location(move_dto[_LOCATION])


def exception_to_dto(api_exception):
    """ Maps an ApiException instance to a DTO to be transferred by the API """
    return {
        _KEY: api_exception.key,
        _MESSAGE: api_exception.message,
    }


def _player_to_dto(player: Player):
    """Maps a player to a DTO

    :param player: an instance of model.Player
    :return: a structure whose JSON representation is valid for the API
    """
    return {_ID: player.identifier,
            _MAZE_CARD_ID: player.maze_card.identifier}


def _maze_card_to_dto(maze_card: MazeCard, location: BoardLocation = None):
    """ Maps a maze card to a DTO

    :param maze_card: an instance of model.MazeCard
    :param location: an instance of BoardLocation, i.e. the location of this card on the board.
    if no location is given, the card is not on the board, i.e. it is the leftover card.
    :return: a structure whose JSON representation is valid for the API
    """
    return {_ID: maze_card.identifier,
            _DOORS: maze_card.doors,
            _ROTATION: maze_card.rotation,
            _LOCATION: _board_location_to_dto(location)}


def _board_location_to_dto(location: BoardLocation):
    """ Maps a board location to a DTO

    :param location: an instance of model.BoardLocation
    :return: a structure whose JSON representation is valid for the API
    """
    if location is None:
        return None
    return {_ROW: location.row,
            _COLUMN: location.column}


def _dto_to_player(player_dto, maze_card_dict):
    """ maps a DTO to a player

    :param player_dto: a dictionary representing the API (sub-)structure of a player
    :param maze_card_dict: a dictionary between maze card ids and MazeCard instances
    :raises KeyError: if maze_card_dict does not contain the maze card id in player_dto
    :return: a Player instance
    """
    return Player(player_dto[_ID], maze_card_dict[player_dto[_MAZE_CARD_ID]])


def _dto_to_maze_card(maze_card_dto):
    """ Maps a DTO to a maze card and a board location

    :param maze_card_dto: a dictionary representing the API (sub-)structure of a maze card
    :return: a MazeCard instance and a BoardLocation instance (or None, for the leftover card)
    """
    maze_card = MazeCard(maze_card_dto[_ID], maze_card_dto[_DOORS], maze_card_dto[_ROTATION])
    location = _dto_to_board_location(maze_card_dto[_LOCATION])
    return maze_card, location


def _dto_to_board_location(board_location_dto):
    """ Maps a DTO to a board location

    :param board_location_dto: a dictionary for the API (sub-)structure of a board location, or None
    :return: a BoardLocation instance, or None
    """
    if board_location_dto is None:
        return None
    return BoardLocation(board_location_dto[_ROW], board_location_dto[_COLUMN])
