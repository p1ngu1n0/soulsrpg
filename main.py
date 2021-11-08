from soulsrpg.soulsrpg import Game

def main() -> int:
    g = Game("Hello pygame", (500, 500))
    g.run()
    return 0

if __name__ == "__main__":
    exit(main())
