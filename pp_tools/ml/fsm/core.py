# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:09:24 2022

@author: pepemxl

StateMachine implementation based on transitions library

- Context - it is the original class of our application. 
    It maintains a reference to one of the concrete states on which its behavior depends. 
    It also has a method to modify the internal state.
-  State interface - All supported states share the same state interface. 
    Only the state interface allows Context to communicate with state objects. 
    Context can only communicate with state objects via the state interface.
-  Concrete states - For each state, these objects implement the 'State' interface. 
    These are the main objects which contain the state-specific methods. 
"""


from collections import OrderedDict, defaultdict, deque
from enum import Enum, EnumMeta
from typing import Union, Optional
import itertools
import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def listify(obj:object) -> Union[list, tuple]:
    """ Wraps a passed object into a list in case it has not been a list or a 
    tuple before.
    Returns an empty list in case "obj" is None.
    Args:
        obj: Object to be wrapped into list.
    Returns:
        list or tuple: return a tuple in case "obj" is a tuple.
    """
    if obj is None:
        return []

    try:
        if isinstance(obj, (list, tuple, EnumMeta)):
            return obj
        else: 
            return [obj]
    except ReferenceError:
        return [obj]


class Context(object):
    """ Context
    
    """
    def __init__(self,
                name:Union[str, Enum]
                ):
        pass

class State(object):
    """ State
        
    """
    # Static variables to define some common attributes
    # Dynamic methods for states must start with prefix "on_"
    list_dynamic_methods = ['on_enter', 'on_exit']

    def __init__(self, 
                 name:Union[str, Enum], 
                 on_enter:Union[str, list, None]=None, 
                 on_exit:Union[str, list, None]=None,
                 ignore_invalid_triggers:Optional[bool]=None
                 ):
        """
        Args:
            name Union[str, Enum]: The name of the state
            on_enter Union[str, list]: Optional callable(s) to trigger when a
                state is entered. Can be either a string providing the name of
                a callable, or a list of strings.
            on_exit (Union[str, list]: Optional callable(s) to trigger when a
                state is exited. Can be either a string providing the name of a
                callable, or a list of strings.
            ignore_invalid_triggers Optional[bool]: Optional flag to indicate if
                invalid triggers should raise an exception

        """
        if name is None:
            logger.debug("State name None")
        self._name = name
        self.on_enter = listify(on_enter) if on_enter else []
        self.on_exit = listify(on_exit) if on_exit else []
        self.ignore_invalid_triggers = ignore_invalid_triggers

    @property
    def name(self):
        """ 
        Property with the name of the state. 
        Please use camel case on names, in this version don't use spaces.
        """
        if isinstance(self._name, Enum):
            return self._name.name
        return self._name

    @property
    def value(self):
        """ The state's value."""
        return self._name

    def enter(self, event_data):
        """ Triggered when a state is entered. """
        logger.debug("{0}Entering state {1}. Processing callbacks...", event_data.machine.name, self.name)
        event_data.machine.callbacks(self.on_enter, event_data)
        logger.info("%sFinished processing state %s enter callbacks.", event_data.machine.name, self.name)

    def exit(self, event_data):
        """ Triggered when a state is exited. """
        logger.debug("%sExiting state %s. Processing callbacks...", event_data.machine.name, self.name)
        event_data.machine.callbacks(self.on_exit, event_data)
        logger.info("%sFinished processing state %s exit callbacks.", event_data.machine.name, self.name)

    def add_callback(self, trigger, func):
        """ Add a new enter or exit callback.
        Args:
            trigger (str): The type of triggering event. Must be one of
                'enter' or 'exit'.
            func (str): The name of the callback function.
        """
        callback_list = getattr(self, 'on_' + trigger)
        callback_list.append(func)

    def __repr__(self):
        return "<%s('%s')@%s>" % (type(self).__name__, self.name, id(self))


class Condition(object):
    """ A helper class to call condition checks.

    Attributes:
        func (str or callable): The function to call for the condition check
        target (bool): Indicates the target state--i.e., when True,
                the condition-checking callback should return True to pass,
                and when False, the callback should return False to pass.
    """

    def __init__(self, func, target=True):
        """
        Args:
            func (str or callable): Name of the condition-checking callable
            target (bool): Indicates the target state--i.e., when True,
                the condition-checking callback should return True to pass,
                and when False, the callback should return False to pass.
        Notes:
            This class should not be initialized or called from outside a
            Transition instance, and exists at module level (rather than
            nesting under the transition class) only because of a bug in
            dill that prevents serialization under Python 2.7.
        """
        self.func = func
        self.target = target

    def check(self, event_data):
        """ Check whether the condition passes.
        Args:
            event_data (EventData): An EventData instance to pass to the
                condition (if event sending is enabled) or to extract arguments
                from (if event sending is disabled). Also contains the data
                model attached to the current machine which is used to invoke
                the condition.
        """
        predicate = event_data.machine.resolve_callable(self.func, event_data)
        if event_data.machine.send_event:
            return predicate(event_data) == self.target
        return predicate(*event_data.args, **event_data.kwargs) == self.target

    def __repr__(self):
        return "<%s(%s)@%s>" % (type(self).__name__, self.func, id(self))


if __name__=='__main__':
    class MachineLearningModel(object):
        states = ['training', 'validating']
        
    hello_state = State(name='Hello World', on_enter='print', on_exit='exit')
    print(hello_state.name)
    
    
    
    