#!/usr/bin/python3

import json
from collections.abc import MutableMapping, Sequence
from typing import Union, Any

from argparse import ArgumentParser
from nbt.nbt import NBTFile, _TAG_Numeric, TAG_String


def _to_py(x: Any) -> Union[dict, str, list, int]:
    if isinstance(x, (str, int)):
        return x
    if isinstance(x, (_TAG_Numeric, TAG_String)):
        return x.value
    if isinstance(x, (list, Sequence)):
        return [_to_py(y) for y in x]
    if isinstance(x, (dict, MutableMapping)):
        return {_to_py(k): _to_py(v)
                for k, v in x.items()}


def nbt_to_json(filename: str, **dumps_kwargs: dict) -> str:
    nbt = NBTFile(filename)
    py = _to_py(nbt)
    return json.dumps(py, **dumps_kwargs)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pretty", help="Pretty-print output", action="store_true")
    parser.add_argument("--inplace", help="Create JSON files in-place", action="store_true")
    parser.add_argument("files", help="NBT file to jsonify", nargs="+")

    args = parser.parse_args()

    kwargs = {"indent": 4} if args.pretty else {}

    for file in args.files:
        if args.inplace:
            *fname, ext = file.split(".")
            with open(".".join(fname) + ".json", "w") as f:
                f.write(nbt_to_json(file, **kwargs))
        else:
            print(nbt_to_json(file, **kwargs))
