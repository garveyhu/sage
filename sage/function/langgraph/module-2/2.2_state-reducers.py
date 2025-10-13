from operator import add
from typing import Annotated, TypedDict


class State(TypedDict):
    foo: Annotated[list[int], add]
