from typing import Annotated

def double(x: int) -> int:
    return x * 2

def double_2(x: Annotated[int, (0, 100)]) -> int:
    return x * 2

result = double_2(111)
print(result)