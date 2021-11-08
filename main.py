import soulsrpg
# NOTE(cdecompilador): Need this long path, otherwise tests need to import also OpenGL
from soulsrpg.utils import Game

def main() -> int:
    Game("Hello pygame", (500, 500), None).run()
    return 0

if __name__ == "__main__":
    exit(main())
