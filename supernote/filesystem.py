# Written referencing https://benhoyt.com/writings/pygit/ along the way!

from __future__ import annotations
from typing import Tuple

import os
import hashlib
import zlib
import enum


class ObjectType(enum.Enum):

    snapshot = 1
    tree = 2
    blob = 3


def metadata_path(*subpath: str) -> os.PathLike:
    return os.path.join(".metadata", *subpath)


def init_workspace():
    """
    Initialise the workspace with a .metadata directory.
    """

    # Create .metadata directory
    try:
        print("Initialising workspace...")
        os.mkdir(metadata_path())
        os.mkdir(metadata_path("objects"))
        os.mkdir(metadata_path("heads"))
        os.mkdir(metadata_path("refs"))
    except FileExistsError:
        print("Workspace already initialised!")


def hash_object(data: bytes, obj_type: ObjectType, write: bool = False) -> str:
    """
    Calculates the SHA-1 hash of some data, and
    write it to the object directory if write is True.
    """

    header = f"{obj_type.value} {len(data)}".encode()
    full_data = header + b"\0" + data
    sha1 = hashlib.sha1(full_data).hexdigest()

    if write:
        path = metadata_path("objects", sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(zlib.compress(full_data))

    return sha1


def find_object(sha1: str) -> os.PathLike:
    """
    Find an object with the given SHA-1 hash,
    return the path to that object.
    Raises ValueError if there are no objects that match.
    """

    if len(sha1) < 2:
        raise ValueError("hash must be 2 or more characters!")

    obj_dir = metadata_path("objects", sha1[:2])
    objects = [name for name in os.listdir(obj_dir) if name.startswith(sha1[2:])]

    if not objects:
        raise ValueError(f"object {sha1} not found!")
    if len(objects) >= 2:
        raise ValueError(f"multiple ({len(objects)}) objects with prefix {sha1}!")

    return os.path.join(obj_dir, objects[0])


def read_object(sha1: str) -> Tuple[ObjectType, bytes]:
    """
    Find an object with the given SHA-1 hash,
    return the data contained.
    """

    path = find_object(sha1)
    full_data = None
    with open(path, "rb") as f:
        full_data = zlib.decompress(f.read())
    null_index = full_data.index(b"\0")
    header = (int(i) for i in full_data[:null_index].decode().split())
    obj_type, size = header
    data = full_data[null_index+1:]
    assert int(size) == len(data), f"expected size {size}, got {len(data)} bytes!"
    return ObjectType(obj_type), data
