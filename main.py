#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# NOTE(cdecompilador): Need this long path, otherwise tests need to import also OpenGL
# __autor__ = ["p1ngu1n0", "cdecompilador"]

from soulsrpg.utils import Director
from soulsrpg.scenes import lvl1


def main() -> int:
    Director(lvl1()).loop()
    return 0


if __name__ == "__main__":
    exit(main())
