import collections.abc as clcs
from types import FunctionType, LambdaType
from typing import Literal

# for typehinting purposes, only because i dont want to deal with the bullshit that is circular imports.

# IsColor = pygame.Color | str | clcs.Sequence[int, int, int] | clcs.Sequence[int, int, int, int]
# IsFunction = FunctionType | LambdaType
# IsPosition = clcs.Sequence[int, int]
# IsSizeSequence = clcs.Sequence[int, int]
# IsOrientLiteral = Literal['vertical', 'horizontal']
# IsFont = pygame.font.Font | pygame.font.FontType
#
# from natrium.widgetsBETA import Panel
# from natrium.display import Window
#
# IsContainer = Panel | Window

IsOrientLiteral = "Literal['vertical', 'horizontal']"
IsPosition = IsSizeSequence = 'Sequence[int, int]'
IsContainer = 'Panel | Window'
IsColor = 'Color | str | Sequence[int, int, int] | Sequence[int, int, int, int]'
Event = 'Event'
IsFunction = 'IsFunction'
IsFont = 'IsFont'