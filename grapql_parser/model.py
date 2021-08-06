from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Any, Union


class OperationType(Enum):
    QUERY = 'QUERY'
    MUTATION = 'MUTATION'
    SUBSCRIPTION = 'SUBSCRIPTION'


@dataclass
class Fragment:
    pass


@dataclass
class NamedType:
    type_name: str


@dataclass
class ListType:
    type: Type


@dataclass
class NonNullType:
    type: Union[NamedType, ListType]


Type = Union[NamedType, ListType, NonNullType]


@dataclass
class Variable:
    name: str
    type: Union[NamedType, ListType, NonNullType]
    default_value: Any


@dataclass
class Operation:
    operation_type: OperationType
    variables: Optional[List[Variable]] = None
    directives: Optional[str] = None
    selection_set: Optional[str] = None
    name: Optional[str] = None


@dataclass
class GraphqlDocument:
    fragments: List[Fragment]
    operations: List[Operation]