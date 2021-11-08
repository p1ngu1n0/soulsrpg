import soulsrpg
from soulsrpg.utils import Scene 

def main() -> int:
    soulsrpg.Game("Hello pygame", (500, 500), Scene()).run()
    return 0

if __name__ == "__main__":
    exit(main())
