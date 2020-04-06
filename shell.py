from family_tree import FamilyTree


class Shell:
    start_sign = '> '
    exit_command = 'exit'
    query_command = '?-'
    cmd_pattern = '<subject> <predicate> [objects] | <?-> <query> | exit | table'

    def __init__(self, database: str = None, program: str = None):
        self.family_tree = FamilyTree()

        if program is not None:
            self.execute_file(program)
        status = None
        if database is not None:
            status = self.parse_file(database)
        if status != 'exit':
            self.main_loop()

    def parse_command(self, command: str):
        command = command.strip('\n')
        if not len(command):
            return
        if command == 'table':
            self.family_tree.print_as_table()

        args = command.split()
        if len(args) < 2:
            raise ValueError(f'Incorrect format. Use follow pattern: {self.cmd_pattern}')

        if args[0] == self.query_command:
            self.family_tree.query(' '.join(args[1:]))
        else:
            self.family_tree.apply(args[1], [args[0]] + args[2:])

    def parse_file(self, file):
        with open(file) as f:
            lines = f.readlines()
            for command in lines:
                if command == self.exit_command:
                    break
                try:
                    self.parse_command(command)
                except Exception as e:
                    print(f'[Error] {e}')
        return command  # return last executed command

    def execute_file(self, file):
        self.family_tree.consult(file)

    def main_loop(self):
        command = input(self.start_sign)
        while command != self.exit_command:
            try:
                self.parse_command(command)
            except Exception as e:
                print(f'[Error] {e}')
            command = input(self.start_sign)
        print('Bye!')

