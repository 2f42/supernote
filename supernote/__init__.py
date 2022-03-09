import click

from .filesystem import init_workspace, hash_object, read_object, ObjectType


@click.group()
def cli():
    pass


@cli.command()
def init():
    init_workspace()
    print(hash_object(b"hello!", ObjectType.blob, True))


@cli.command()
def read():
    obj_type, data = read_object(hash_object(b"hello!", ObjectType.blob))
    print(obj_type, data)
