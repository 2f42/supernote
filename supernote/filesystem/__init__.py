import os

from .filesystem import Filesystem

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_fs():
    if "fs" not in g:
        g.fs = Filesystem(os.path.join(current_app.instance_path, "fs"))

    return g.fs


def close_fs(e=None):
    fs = g.pop("fs", None)

    if fs is not None:
        pass


def init_fs():
    fs = get_fs()

    print("Initialising filesystem!")
    fs.clean()
    fs.init_directories()


@click.command("init-fs")
@with_appcontext
def init_fs_command():
    """Clear the existing filesystem and create required tables"""
    init_fs()
    click.echo("Initialised the filesystem.")


def init_app(app):
    app.teardown_appcontext(close_fs)
    app.cli.add_command(init_fs_command)
