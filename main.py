import argparse

from shell import Shell


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--database', type=str, help='Path to file with knowledge', default=None)
    parser.add_argument('--program', type=str, help='Path to file with prolog program', default=None)
    args = parser.parse_args()

    Shell(
        database=args.database,
        program=args.program
    )


if __name__ == '__main__':
    main()
