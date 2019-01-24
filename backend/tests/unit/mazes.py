""" This module serves as a storage for maze strings """

MINIMAX_BIG_COMPONENT_MAZE = """
###|#.#|#.#|###|#.#|#.#|###|
#..|#..|...|...|#..|..#|..#|
#.#|###|###|#.#|###|###|#.#|
---------------------------|
###|###|#.#|#.#|#.#|#.#|#.#|
...|...|#.#|#..|#.#|...|..#|
#.#|#.#|#.#|###|#.#|###|#.#|
---------------------------|
#.#|#.#|#.#|#.#|#.#|#.#|#.#|
#..|#..|..#|#..|..#|#.#|..#|
#.#|#.#|#.#|#.#|#.#|#.#|#.#|
---------------------------|
#.#|#.#|#.#|###|#.#|###|###|
..#|..#|#..|...|...|...|..#|
###|#.#|###|#.#|###|#.#|#.#|
---------------------------|
###|#.#|###|#.#|###|#.#|###|
#..|..#|#..|#.#|...|#..|...|
#.#|###|#.#|#.#|#.#|###|###|
---------------------------|
###|#.#|###|#.#|#.#|#.#|#.#|
..#|#..|...|...|#.#|#..|..#|
#.#|#.#|###|###|#.#|#.#|#.#|
---------------------------|
#.#|#.#|###|###|#.#|#.#|#.#|
#..|...|...|...|#.#|#..|..#|
###|###|#.#|###|#.#|###|###|
---------------------------*
"""

MINIMAX_DIFFICULT_MAZE = """
###|#.#|###|###|#.#|#.#|###|
#..|#..|...|#..|#..|#..|..#|
#.#|###|#.#|#.#|###|#.#|#.#|
---------------------------|
#.#|#.#|#.#|###|#.#|#.#|###|
#..|..#|..#|...|#..|#.#|...|
###|###|#.#|###|###|#.#|###|
---------------------------|
#.#|###|#.#|#.#|###|###|#.#|
#..|#..|#..|#.#|...|...|..#|
#.#|#.#|#.#|#.#|#.#|###|#.#|
---------------------------|
###|#.#|###|#.#|###|###|###|
...|..#|#..|#.#|#..|...|...|
###|#.#|#.#|#.#|#.#|###|###|
---------------------------|
#.#|#.#|#.#|#.#|#.#|###|#.#|
#..|#..|#..|#.#|..#|...|...|
#.#|###|#.#|#.#|#.#|###|###|
---------------------------|
###|#.#|#.#|#.#|#.#|#.#|#.#|
..#|#..|#..|...|#.#|#..|..#|
#.#|###|#.#|###|#.#|#.#|#.#|
---------------------------|
#.#|###|###|###|#.#|#.#|#.#|
#..|...|#..|...|#.#|...|..#|
###|###|#.#|###|#.#|###|###|
---------------------------*
"""

MINIMAX_BUG_MAZE = """
###|#.#|###|###|###|#.#|###|
#..|#.#|...|..#|...|#.#|..#|
#.#|#.#|#.#|#.#|#.#|#.#|#.#|
---------------------------|
#.#|#.#|#.#|#.#|#.#|#.#|#.#|
#..|#..|#..|#.#|#..|#..|#.#|
#.#|###|#.#|#.#|###|###|#.#|
---------------------------|
#.#|#.#|#.#|#.#|###|###|#.#|
#..|#..|#..|#..|...|...|..#|
#.#|###|#.#|###|#.#|###|#.#|
---------------------------|
###|#.#|###|#.#|#.#|#.#|#.#|
...|#..|...|..#|..#|#..|#.#|
###|###|#.#|#.#|#.#|###|#.#|
---------------------------|
#.#|#.#|#.#|#.#|#.#|#.#|#.#|
#..|#..|...|#..|..#|#..|..#|
#.#|###|###|###|#.#|###|#.#|
---------------------------|
#.#|#.#|#.#|#.#|#.#|###|#.#|
#..|#..|#..|#.#|#.#|#..|#.#|
###|#.#|###|#.#|#.#|#.#|#.#|
---------------------------|
#.#|#.#|#.#|#.#|#.#|#.#|#.#|
#..|#.#|...|#..|...|#.#|..#|
###|#.#|###|###|###|#.#|###|
---------------------------|
"""

GENERATED_WITH_LINE_LEFTOVER = """
###|#.#|###|#.#|###|###|###|
#..|#.#|...|..#|...|...|..#|
#.#|#.#|#.#|###|#.#|###|#.#|
---------------------------|
###|###|#.#|#.#|###|###|###|
..#|...|#.#|..#|..#|...|#..|
#.#|###|#.#|#.#|#.#|#.#|#.#|
---------------------------|
#.#|###|#.#|#.#|###|###|#.#|
#..|...|#..|#.#|...|...|..#|
#.#|###|#.#|#.#|#.#|###|#.#|
---------------------------|
#.#|###|#.#|#.#|###|#.#|###|
#..|..#|#..|#..|...|#.#|...|
#.#|#.#|###|###|#.#|#.#|###|
---------------------------|
#.#|###|#.#|###|#.#|###|#.#|
#..|..#|...|..#|..#|..#|..#|
#.#|#.#|###|#.#|#.#|#.#|#.#|
---------------------------|
#.#|#.#|###|#.#|###|###|###|
#..|#..|..#|#.#|..#|...|...|
#.#|###|#.#|#.#|#.#|###|###|
---------------------------|
#.#|###|#.#|#.#|#.#|#.#|#.#|
#..|..#|...|#..|...|#..|..#|
###|#.#|###|###|###|#.#|###|
---------------------------*
"""