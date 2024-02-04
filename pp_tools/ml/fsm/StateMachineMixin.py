# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 08:34:25 2022

@author: pepemxl
"""
import typing
from dataclasses import dataclass

from .StateMachine import Machine


@dataclass
class StateConfig:
    initial: typing.Any
    states: typing.List[t.Any]
    transitions: typing.Optional[typing.List[typing.List[typing.Any]]]
    state_attribute: typing.Optional[str] = "state"
    status_attribute: typing.Optional[str] = "status"
    machine_name: typing.Optional[str] = "machine"
    after_state_change: typing.Optional[typing.Any] = None


@dataclass
class StateMixin:
    state_config: StateConfig

    @property
    def state(self):
        return getattr(self, self.state_config.status_attribute)

    @state.setter
    def state(self, value):
        setattr(self, self.state_config.status_attribute, value)

    @classmethod
    def init_state_machine(cls, obj, *args, **kwargs):
        machine = Machine(
            model=obj,
            states=cls.state_config.states,
            transitions=cls.state_config.transitions,
            initial=getattr(obj, obj.state_config.status_attribute) or cls.state_config.initial,
            model_attribute=cls.state_config.state_attribute,
            after_state_change=cls.state_config.after_state_change,
        )

        setattr(obj, cls.state_config.machine_name, machine)