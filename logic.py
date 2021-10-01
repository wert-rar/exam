# analog for -> operator
arrow = lambda A, B: int(not (A > B))


# LTS -- LogicTableSolver

class BaseLTS:
    '''
    Class with basic functions for LTS

    create logic  table for <n> x
    create title for <n> x
    print table
    '''

    def __init__(self, number_of_x):
        self.n = number_of_x

    @staticmethod
    def create_column(n, length):
        # count of zero and count of ones in one pare
        zero, one = [], []
        row = []

        count = 2 ** (n - 1)
        # fill the pare with require count of numbers
        for i in range(count):
            zero.append(0)
            one.append(1)
        # count of pares of zeros and ones
        count_of_no = length // (count * 2)

        for i in range(count_of_no):
            row.extend(zero)
            row.extend(one)

        return row

    @staticmethod
    def create_var_table(n):
        table = []
        len_ = 2 ** n
        for i in range(n, 0, -1):
            table.append(BaseLTS.create_column(i, len_))
        return table

    # title for table
    @staticmethod
    def create_title(n):
        form = ''
        for i in range(n):
            form += f'x{i + 1}  '
        form += 'F'
        return form

    # print table
    @staticmethod
    def print_table(n, table):
        print(BaseLTS.create_title(n))
        form = '{}   ' * n
        for i in range(2 ** n):
            table_row = [t[i] for t in table]
            print(
                form.format(*table_row))

    # print table and answers or calculate answers automatically
    @staticmethod
    def print_log_table(n, table, fs):

        print(BaseLTS.create_title(n))
        form = '{}   ' * (n + 1)
        # if we have list of answers we only write answers
        if isinstance(fs, list):
            for i in range(2 ** n):
                table_row = [t[i] for t in table]
                print(form.format(*table_row, fs[i]))
        # else we calculate and write answer
        else:
            for i in range(2 ** n):
                table_row = [t[i] for t in table]
                print(form.format(*table_row, fs(*table_row)))

    # base method for Child's classes
    def solve(self):
        table = self.create_var_table(self.n)
        print("gen table with all possible all_ways")
        self.print_table(self.n, table)


class OneFormulaLTS(BaseLTS):
    '''
    Solve log table for one formula
    '''
    def __init__(self, number_of_x, formula):
        super().__init__(number_of_x)
        self.formula = formula
        self.table = self.create_var_table(number_of_x)

    def create_log_table(self):
        f_column = []
        for i in range(2 ** self.n):
            table_row = [t[i] for t in self.table]
            f_column.append(int(
                self.formula(*table_row)
            ))

        return f_column

    def solve(self):
        print("gen all possible variations of formula")
        self.print_log_table(
            self.n,
            self.table,
            self.create_log_table(),
        )


class LotFormulaLTS(BaseLTS):
    def __init__(self, number_of_x, formulas, pattern=None, giving_table=None):
        super().__init__(number_of_x)
        self.giving_table = giving_table
        self.formulas = formulas
        self.pattern = pattern

    def normalize_giving_table(self):
        # create all possible variations of arguments
        table = self.create_var_table(self.n)
        compared_table = []

        for row in self.giving_table:
            for i in range(2 ** self.n):
                table_row = [t[i] for t in table]

                # if row already in table we don't need check it again
                # if row  have less ones or less zeros, it can't be in compare_table
                if table_row not in compared_table and \
                        table_row.count(1) >= row.count(1) and \
                        table_row.count(0) >= row.count(0):
                    compared_table.append(table_row)

        self.giving_table = compared_table

    def compare_formulas(self):

        ind = None
        correct = []

        if len(self.pattern) != len(self.giving_table[0]):
            print("Error! \nnumber of answers != rows of table")
            print(len(self.pattern))
            print(len(self.giving_table))
            return

        # Get result for each formula and compare with expected answer
        for f in self.formulas:

            answer = []
            # collect answers of formula
            for i in range(len(self.giving_table)):
                table_row = self.giving_table[i]
                print(table_row, f(*table_row))
                answer.append(int(f(*table_row)))
            print('----------')
            # get correct answer
            if answer == self.pattern:
                ind = self.formulas.index(f)
                correct = answer
        print(f'\nthe right formula is {ind} \nanswers: {correct}')

    def solve(self):

        if self.giving_table is None and self.formulas is None:
            print('cant find right answer in Nothing')

        elif self.formulas is None:
            print('cant build answer without formulas')

        elif self.giving_table is None:
            print('Automatically create Logic Table\n')
            print('Start solving')

            self.giving_table = self.create_var_table(self.n)
            self.compare_formulas()
        else:
            print('Start solving')

            # self.normalize_giving_table()
            self.compare_formulas()


class FinderLTS(OneFormulaLTS):
    '''Find '''
    def __init__(self, number_of_x, f, giving_table):
        super().__init__(number_of_x, f)
        self.giving_table = giving_table

    def compare_with_table(self, table, fs):
        # First study - find not match parts

        compare_table = []
        compare_f = []
        for row in self.giving_table:
            for i in range(2 ** self.n):
                # if we get incorrect answer we don't  compare all Vars
                if row[-1] == fs[i]:
                    table_r = [t[i] for t in table]
                    if table_r.count(1) >= row[0:-1].count(1) and \
                            table_r.count(0) >= row[0:-1].count(0):
                        if table_r not in compare_table:
                            compare_table.append(table_r)
                            compare_f.append(fs[i])
        return compare_table, compare_f

    def print_compare_table(self, com_table, com_f):
        print(self.create_title(self.n))
        form = '{}   ' * (self.n + 1)
        for i in range(len(com_f)):
            print(form.format(*com_table[i], com_f[i]))

    def solve(self):
        table = self.create_var_table(self.n)
        fs = self.create_log_table()
        print('Full Vars Table')
        self.print_log_table(self.n, table, fs)
        if self.giving_table is not None:
            print('\nFind all matches\n')
            ct, cf = self.compare_with_table(table, fs)
            self.print_compare_table(ct, cf)


# EXAMPLES
def lts_test():
    n = 4
    solver = BaseLTS(n)
    solver.solve()


def formul_lts_test():
    f = lambda x, y, z: (((not x) and y) or x) and z
    formul = OneFormulaLTS(3, f)
    formul.solve()


def lot_lts_test():
    table = [[1, 0, 0],
             [1, 0, 1],
             [1, 1, 0]]
    f = lambda x, y, z: ((not x) or z) and y
    f2 = lambda x, y, z: (x and not y) or z
    f4 = lambda x, y, z: (not x or y) or not z
    f3 = lambda x, y, z: (x and y) and not z
    lot_formul = LotFormulaLTS(3, [f, f2, f3, f4], giving_table=table, pattern=[1, 0, 1])
    lot_formul.solve()


def finder_lts_test():
    # First with gen args

    # table = BaseLTS.create_var_table(2)
    # finder = FinderLTS(2, arrow, table)
    # finder.solve()

    # Second with giving table
    table = [
        [None, None, 1],
        [None, 1, 1],
        [0, None, 1],
        [1, 0, 0],
    ]
    finder = FinderLTS(2, arrow, table)
    finder.solve()


def main():
    print('base test')
    lts_test()
    print()
    print('one formul test')
    formul_lts_test()
    print()
    print('lot test')
    lot_lts_test()
    print()
    print('finder test')
    finder_lts_test()


if __name__ == '__main__':
    main()
