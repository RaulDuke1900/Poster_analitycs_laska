import math
import pprint
from typing import Tuple

print('Hello word!')

def foo(x: int) -> Tuple[int, float]:
    return x, math.pi

pprint.pprint('Hello')

print(foo(4))