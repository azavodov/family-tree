from datetime import datetime

from pyswip import Prolog


class FamilyTree:

    def __init__(self):
        self.prolog = Prolog()
        self.apply('current_year', [str(datetime.today().year)])

    def apply(self, predicate, args: list):
        self.prolog.assertz(f"{predicate}({','.join(args)})")

    def query(self, query: str):
        for item in self.prolog.query(query):
            for key in item.keys():
                print(f'\t {key} = {item[key]} ; \t', end='')
            print()

    def consult(self, prolog_program_file: str):
        self.prolog.consult(prolog_program_file)

    def print_as_table(self):
        print(list(self.prolog.query()))
