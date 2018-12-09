#### object, objectives
Items placed on maze cards. The player has to reach them with their playing piece to win the game.
#### maze card
The cards or tiles the game board consists of.
#### pathways
The graph built out of all subpaths. Players can only move along those pathways.
#### game board
The set of all maze cards placed in a two-dimensional matrix of size 7x7
#### leftover maze card
One maze card which is not situated on the game board, but remains on the edge of the board.
#### shifting action
Insert a maze card, push out a maze card on the opposite side. This forms new pathways.
#### piece
Playing pieces of the players. Always situated on the game board.
#### turn
A player's turn consists of a shifting action followed by a move action.
#### no-pushback rule
Game rule which prohibits players make a shifting action which reverses the shifting action of the previous player's turn.
#### door
a maze card's openings to its surrounding cards. If and only if two neighboring maze cards have a door facing the respective other, there is a path between them.
#### subpath
The connections between a single maze card and its neighbors