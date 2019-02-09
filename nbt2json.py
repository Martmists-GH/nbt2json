#!/usr/bin/python3
import json
from typing import Union, Any

from argparse import ArgumentParser
from nbt.nbt import NBTFile, TAG_List, TAGLIST, TAG_Compound, TAG_Int_Array


class Token:
    def __init__(self, type_, name, value, extra=None):
        self.__is_set = False
        self.type_ = type_
        self.name = name
        self._value = value if value is None else _to_py(value)
        self.extra = extra

        if self.type_ == TAG_Compound:
            self.keys = [x.name for x in self._value]

        self.__is_set = True

    def __setattr__(self, key, value):
        if key == "_Token__is_set" or not self.__is_set:
            super().__setattr__(key, value)

        elif key == "_value":
            if not isinstance(self._value, (int, str, float, list)):
                self._value._value = value
            else:
                self._value = value

        elif hasattr(self, "keys") and key in self.keys:
            item = self[key]
            item._value = value

    def __getattr__(self, item):
        if self.__is_set:
            if item in self.keys:
                return self[item]

    def __getitem__(self, key):
        return {x.name: x for x in self._value}[key]

    @property
    def value(self):
        if self.type_ in (float, int, str):
            return self._value

        if self.type_ == list:
            tag = TAG_Compound(self.name)
            tag.tags = [x.value for x in self._value]
            return tag

        if self.type_ == NBTFile:
            x = NBTFile()
            x.name = self.name
            x.tags = [x.value for x in self._value]
            return x

        if self.type_ == TAG_Compound:
            tag = TAG_Compound(name=self.name)
            tag.tags = [x.value for x in self._value]
            tag.name = self.name
            return tag

        if self.type_ == TAG_Int_Array:
            tag = TAG_Int_Array(name=self.name)
            tag.value = self._value
            return tag

        if self.type_ == TAG_List:
            tag = TAG_List(type=self.extra, name=self.name)
            tag.tags = [x.value for x in self._value]
            tag.name = self.name
            return tag

        return self.type_(value=self._value, name=self.name)

    @property
    def cls_name(self):
        return self.type_.__name__ + (f"[{self.extra.__name__}, {self.name}]" if self.extra else f"[{self.name}]")

    @property
    def as_dict(self):
        if issubclass(self.type_, TAG_Compound):
            return {x.name: x.as_dict for x in self._value}

        if issubclass(self.type_, TAG_List):
            return [x.as_dict for x in self._value]

        return self._value

    def __repr__(self):
        return f"{self.cls_name}({self.name or 'value'}={self._value})"

    @property
    def py(self):
        return self.value


def _to_py(x: Any) -> Union[Token, str, int, float, list]:
    if isinstance(x, TAG_Compound):
        return Token(TAG_Compound, x.name, x.tags)
    elif isinstance(x, TAG_List):
        return Token(TAG_List, x.name, x.tags, TAGLIST[x.tagID])
    elif isinstance(x, (str, int, float)):
        return x
    elif isinstance(x, list):
        return [_to_py(y) for y in x]
    else:
        return Token(x.__class__, x.name, x.value if x.value is not None else x.tags)


def nbt_to_json(filename: str, **dumps_kwargs: dict) -> str:
    nbt = NBTFile(filename)
    py = _to_py(nbt)
    return json.dumps(py.as_dict, **dumps_kwargs)


def nbt_to_tree(filename: str) -> Token:
    nbt = NBTFile(filename)
    return _to_py(nbt)


def tree_to_nbt(nbt: Token, filename: str):
    nbt_file = nbt.value
    nbt_file.write_file(filename)


def main():
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


if __name__ == "__main__":
    main()
