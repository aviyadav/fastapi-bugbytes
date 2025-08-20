from typing import Annotated, get_type_hints, get_origin, get_args
from functools import wraps

def check_value_range(func):
    @wraps(func)
    def wrapper(x: int) -> int:
        type_hints = get_type_hints(func, include_extras=True)
        hint = type_hints['x']
        if get_origin(hint) is Annotated:
            hint_type, *hint_args = get_args(hint)
            low, high = hint_args[0]
            if not low <= x <= high:
                raise ValueError(f"x must be between {low} and {high}")
        return func(x)
    return wrapper

def double(x: int) -> int:
    return x * 2

@check_value_range
def double_2(x: Annotated[int, (0, 100)]) -> int:
    return x * 2

result = double_2(111)
print(result)

# result = double_2(53)
# print(result)