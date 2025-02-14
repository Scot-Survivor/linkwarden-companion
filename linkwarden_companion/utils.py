import click

from typing import TypeVar

T = TypeVar('T')


def get_all_subclasses(cls: T):
    """Return all subclasses of a class"""
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_all_subclasses(s)]


def command_tree(obj):
    if isinstance(obj, click.Group):
        return {name: command_tree(value)
                for name, value in obj.commands.items()}
