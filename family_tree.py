from datetime import datetime
from prettytable import PrettyTable

from pyswip import Prolog


class FamilyTree:

    def __init__(self):
        self.prolog = Prolog()
        self.predicates = list()
        self.table = list()
        self.apply([str(datetime.today().year), 'current_year'])

    def apply(self, args: list):
        args[0], args[1] = args[1], args[0]
        predicate = f"{args[0]}({','.join(args[1:])})"
        self.prolog.assertz(predicate)
        self.predicates.append(predicate)
        args[0], args[1] = args[1], args[0]
        self.table.append(args)

    def query(self, query: str):
        for item in self.prolog.query(query):
            for key in item.keys():
                print(f'\t {key} = {item[key]} ; \t', end='')
            print()

    def consult(self, prolog_program_file: str):
        self.prolog.consult(prolog_program_file)

    def remove_last_predicate(self):
        last_predicate = self.predicates[-1]
        self.prolog.retract(last_predicate)
        del self.predicates[-1]
        del self.table[-1]

    def print_as_table(self):
        columns = max([len(row) for row in self.table])
        headers = ['Subject', 'Predicate'] + [f'Object-{i}' for i in range(columns - 2)]
        t = PrettyTable(headers)
        for row in self.table:
            t.add_row(row + ['' for _ in range(len(headers) - len(row))])
        print(t)
