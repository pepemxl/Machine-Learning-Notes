# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:12:35 2022

@author: Jose Alonzo
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, ClassVar, Generator, Iterable, Optional, Sequence, Type

if sys.version_info >= (3, 8):
    from typing import Literal, Protocol, TypedDict
else:
    from typing_extensions import Literal, Protocol, TypedDict


VariableDefinition = TypedDict(
    "VariableDefinition",
    {
        "type": str,
        "field": str,
        "variable name": str,
        "corpus": Iterable[Union[str, Collection[str]]],
        "comparator": Callable[
            [Any, Any], Union[int, float]
        ],  # a custom comparator can only return a single float or int
        "categories": List[str],
        "interaction variables": List[str],
        "has missing": bool,
        "name": str,
    },
    total=False,
)


class Variable(object):
    name: str
    type: ClassVar[str]
    predicates: list[predicates.Predicate]
    higher_vars: Sequence["Variable"]

    def __len__(self) -> int:
        return 1

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        other_name: str = other.name
        return self.name == other_name

    def __init__(self, definition: VariableDefinition):

        if definition.get("has missing", False):
            self.has_missing = True
            try:
                exists_pred = predicates.ExistsPredicate(definition["field"])
                self.predicates.append(exists_pred)
            except KeyError:
                pass
        else:
            self.has_missing = False

    def __getstate__(self) -> dict[str, Any]:
        odict = self.__dict__.copy()
        odict["predicates"] = None

        return odict

    @classmethod
    def all_subclasses(
        cls,
    ) -> Generator[tuple[Optional[str], Type["Variable"]], None, None]:
        for q in cls.__subclasses__():
            yield getattr(q, "type", None), q
            for p in q.all_subclasses():
                yield p


class DerivedType(Variable):
    type = "Derived"

    def __init__(self, definition: VariableDefinition):
        self.name = "(%s: %s)" % (str(definition["name"]), str(definition["type"]))
        super(DerivedType, self).__init__(definition)
        
        
        
        
        
        
        