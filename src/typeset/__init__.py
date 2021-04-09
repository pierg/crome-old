from __future__ import annotations

from copy import copy, deepcopy
from itertools import combinations
from typing import Set, Dict, Union, TypeVar, List, Tuple

from type import Types, TypeKinds

AllTypes = TypeVar('AllTypes', bound=Types)


class Typeset(dict):
    """Set of identifier -> AllTypes"""

    def __init__(self, types: Set[AllTypes] = None):

        """Indicates the supertypes relationships for each type in the typeset"""
        self.__super_types: Dict[AllTypes, Set[AllTypes]] = {}

        """Indicates the mutex relationships for the type in the typeset"""
        self.__mutex_types: Set[Set[AllTypes]] = set()

        """Indicates the adjacency relationships for the type in the typeset"""
        self.__adjacent_types: Dict[AllTypes, Set[AllTypes]] = dict()

        if types is not None:
            self.add_elements(types)
        else:
            super(Typeset, self).__init__()

    def __deepcopy__(self: Typeset, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v))
        """Do not perform a deepcopy of the types"""
        for k, v in self.items():
            result[k] = v
        return result

    def __str__(self):
        ret = ""
        for (key, elem) in self.items():
            ret += f"{key}:\t{elem.name}"
            if elem in self.super_types:
                ret += " -> "
                for supertypes in self.super_types[elem]:
                    ret += supertypes.name
            ret += "\n"
        return ret[:-1]

    def __or__(self, element: Union[Typeset, AllTypes]) -> Typeset:
        """ Returns self | element """
        if isinstance(element, Types):
            element = Typeset({element})
        """Shallow copy"""
        new_dict = copy(self)
        new_dict |= element
        return new_dict

    def __sub__(self, element: Union[Typeset, AllTypes]) -> Typeset:
        """ Returns self - element """
        if isinstance(element, Types):
            element = Typeset({element})
        """Shallow copy"""
        new_dict = copy(self)
        for key in element.keys():
            if key in new_dict:
                del new_dict[key]
        return new_dict

    def __and__(self, element: Typeset) -> Typeset:
        """ Returns self &= element """
        pass

    def __ior__(self, element: Union[Typeset, AllTypes]):
        """ Updates self with self |= element """
        if isinstance(element, Types):
            element = Typeset({element})
        for key, value in element.items():
            if key in self:
                # if value is not self[key]:
                #     print(f"Trying to add an element with key '{key}' and value of type '{type(value).__name__}'")
                #     print(f"ERROR:\n"
                #           f"There is already en element with key '{key}' and value of type '{type(self[key]).__name__}'")
                #     raise Exception("Type Mismatch")
                if type(value).__name__ != type(self[key]).__name__:
                    print(f"Trying to add an element with key '{key}' and value of type '{type(value).__name__}'")
                    print(f"ERROR:\n"
                          f"There is already en element with key '{key}' and value of type '{type(self[key]).__name__}'")
                    raise Exception("Type Mismatch")
            if key not in self:
                self.add_elements({value})
        return self

    def __iand__(self, element: Typeset):
        """ Updates self with self &= element """
        pass

    def __isub__(self, element):
        """ Updates self with self -= element """
        pass


    @staticmethod
    def get_instance_ts(specification_ts: Typeset, world_ts: Typeset) -> Typeset:
        new_ts = Typeset()
        new_ts |= specification_ts
        for t in specification_ts.values():
            if t.kind == TypeKinds.LOCATION:
                adjacent_locations = world_ts[t.name].adjacency_set
                for ta in adjacent_locations:
                    for elem in world_ts.values():
                        if type(elem).__name__ == ta:
                            new_ts |= elem
        return new_ts



    def extract_inputs_outputs(self) -> Tuple[Set[Types], Set[Types]]:
        """Returns a set of types in the typeset that are not controllable and controllable"""
        i = set()
        o = set()
        if len(self.values()) > 0:
            for t in self.values():
                if not t.controllable:
                    i.add(t)
                else:
                    o.add(t)
        return i, o

    def extract_inputs_outputs_excluding_context(self) -> Tuple[Set[Types], Set[Types]]:
        """Returns a set of types (excluding contexts) in the typeset that are not controllable and controllable"""
        i = set()
        o = set()
        if len(self.values()) > 0:
            for t in self.values():
                if t.kind == TypeKinds.CONTEXT:
                    continue
                if not t.controllable:
                    i.add(t)
                else:
                    o.add(t)
        return i, o

    def extract_actions(self) -> Set[Types]:
        """Returns a set of types in the typeset that are controllable actions"""
        ret = set()
        if len(self.values()) > 0:
            for t in self.values():
                if t.kind == TypeKinds.ACTION:
                    ret.add(t)
        return ret

    def extract_location(self) -> Set[Types]:
        """Returns a set of types in the typeset that are controllable location"""
        ret = set()
        if len(self.values()) > 0:
            for t in self.values():
                if t.kind == TypeKinds.LOCATION:
                    ret.add(t)
        return ret

    def extract_sensors(self) -> Set[Types]:
        """Returns a set of types in the typeset that are not controllable sensors"""
        ret = set()
        if len(self.values()) > 0:
            for t in self.values():
                if t.kind == TypeKinds.SENSOR:
                    ret.add(t)
        return ret

    def extract_sensor_actions(self) -> Set[Types]:
        """Returns a set of types in the typeset that are sensors of action completion"""
        ret = set()
        if len(self.values()) > 0:
            for t in self.values():
                if t.kind == TypeKinds.SENSOR_ACTION:
                    ret.add(t)
        return ret

    def extract_sensor_locations(self) -> Set[Types]:
        """Returns a set of types in the typeset that are sensors indicating current robot location"""
        ret = set()
        if len(self.values()) > 0:
            for t in self.values():
                if t.kind == TypeKinds.SENSOR_LOCATION:
                    ret.add(t)
        return ret

    def add_elements(self, types: Set[AllTypes]):
        if types is not None:
            for elem in types:
                super(Typeset, self).__setitem__(elem.name, elem)

        self.update_subtypes()
        self.update_mutextypes()
        self.update_adjacenttypes()

    def update_subtypes(self):
        if len(self.values()) > 1:
            for (a, b) in combinations(self.values(), 2):
                if isinstance(a, type(b)):
                    if a in self.__super_types:
                        self.__super_types[a].add(b)
                    else:
                        self.__super_types[a] = {b}
                if isinstance(b, type(a)):
                    if b in self.__super_types:
                        self.__super_types[b].add(a)
                    else:
                        self.__super_types[b] = {a}

    def update_mutextypes(self):
        if len(self.values()) > 1:
            self.__mutex_types = set()
            mutex_vars_dict: Dict[str, Set[Types]] = {}
            for variable in self.values():
                if variable.mutex_group != "":
                    if variable.mutex_group in mutex_vars_dict:
                        mutex_vars_dict[variable.mutex_group].add(variable)
                    else:
                        mutex_vars_dict[variable.mutex_group] = set()
                        mutex_vars_dict[variable.mutex_group].add(variable)
            for vars in mutex_vars_dict.values():
                self.__mutex_types.add(frozenset(vars))

    def update_adjacenttypes(self):
        if len(self.values()) > 1:
            self.__adjacent_types = dict()
            for variable in self.values():
                if hasattr(variable, "adjacency_set"):
                    """Adding 'self' as adjacent as well i.e. the robot can stay still"""
                    self.__adjacent_types[variable] = {variable}
                    for adjacent_class in variable.adjacency_set:
                        for variable_candidate in self.values():
                            if variable_candidate.__class__.__name__ == adjacent_class:
                                self.__adjacent_types[variable].add(variable_candidate)

    def __setitem__(self, name, elem):
        self.add_elements({elem})

    @property
    def super_types(self) -> Dict[AllTypes, Set[AllTypes]]:
        return self.__super_types

    @property
    def mutex_types(self) -> Set[Set[AllTypes]]:
        return self.__mutex_types

    @property
    def adjacent_types(self) -> Dict[AllTypes, Set[AllTypes]]:
        return self.__adjacent_types

