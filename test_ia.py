import pytest
import numpy
from ia import *

@pytest.mark.parametrize(
    "tablero, solucion",
[
    ([-1,0,0,1,1,0,0,0,-1], 0),
    ([1,1,0,0,-1,0,0,1,-1], 0),
    ([1,1,-1,0,1,-1,1,-1,-1], 1),
    ([1,1,1,0,-1,0,0,1,-1], 2),
    ([1,1,-1,-1,1,1,1,-1,-1], 3),

]
)

def test_resultadopartida(tablero, solucion):
    assert resultado(np.array(tablero).reshape(3,3)) == solucion;
