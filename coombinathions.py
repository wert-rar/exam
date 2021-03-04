class CombSolver:

    def __init__(self, start: int, end: int, pluses=None, multipliers=None, powers=None, prev=False):
        self.start = start
        self.end = end + 1
        self.all_ways = [1] * (end - start + 1)
        # multiply by
        self.multipliers = multipliers
        self.pluses = pluses
        self.powers = powers
        # get func for calculating ways
        self.calculate_f = self.get_final_function(prev)

    def debug_log(self):
        print('Number      Count of ways')
        for i in range(self.end - self.start):
            print(i + self.start, '       ', self.all_ways[i])

    # will be override in children's--------
    def get_ways_from_pluses(self, n):
        """
        for example:
            plus is 2
            plus2 is 3
            plus3 is 10
            number is 10
        1) 10 - 2 = 8  so we need a count of ways to 8
        2) 10 - 3 = 7  so we need a count of ways to 7
        3)10 - 10 = 0   so we cant get a number if ways
        """
        pass

    def get_ways_from_dels(self, n):
        """
        for example:
            del is 4
            number is 24
            24 / 4 = 6 so we need a count of ways to 6
        """

    def get_ways_from_power(self, n):
        """
        for example:
             del is 4
             number is 24
             24 / 4 = 6 so we need a count of ways to 6
        """

    # check is the current number a (x + x-1)
    def get_ways_from_prev(self, n):

        if n % 2 == 0:
            return 0
        x = (n + 1) / 2
        if x in range(self.start, n):
            return self.all_ways[int(x) - self.start]

    # ---------------------------------------

    # combines checks for factors,summands and squares,
    # eliminates the action if the list is empty
    def get_final_function(self, prev):
        if prev:
            if self.pluses is not None:
                if self.multipliers is not None:
                    if self.powers is not None:
                        return lambda n: self.get_ways_from_pluses(n) + \
                                         self.get_ways_from_dels(n) + \
                                         self.get_ways_from_power(n) + \
                                         self.get_ways_from_prev(n)
                    else:
                        return lambda n: self.get_ways_from_pluses(n) + \
                                         self.get_ways_from_dels(n) + \
                                         self.get_ways_from_prev(n)
                else:
                    if self.powers is not None:
                        return lambda n: self.get_ways_from_pluses(n) + \
                                         self.get_ways_from_power(n) + \
                                         self.get_ways_from_prev(n)
                    else:
                        return lambda n: self.get_ways_from_pluses(n) + \
                                         self.get_ways_from_prev(n)

            else:
                if self.multipliers is not None:
                    if self.powers is not None:
                        return lambda n: self.get_ways_from_dels(n) + \
                                         self.get_ways_from_power(n) + \
                                         self.get_ways_from_prev(n)
                    else:
                        return lambda n: self.get_ways_from_dels(n) + \
                                         self.get_ways_from_prev(n)
                else:
                    if self.powers is not None:
                        return lambda n: self.get_ways_from_power(n) + \
                                         self.get_ways_from_prev(n)
                    else:
                        return lambda n: self.get_ways_from_prev(n)
        else:
            if self.pluses is not None:
                if self.multipliers is not None:
                    if self.powers is not None:
                        return lambda n: self.get_ways_from_pluses(n) + \
                                         self.get_ways_from_dels(n) + \
                                         self.get_ways_from_power(n)
                    else:
                        return lambda n: self.get_ways_from_pluses(n) + \
                                         self.get_ways_from_dels(n)
                else:
                    if self.powers is not None:
                        return lambda n: self.get_ways_from_pluses(n) + \
                                         self.get_ways_from_power(n)
                    else:
                        return lambda n: self.get_ways_from_pluses(n)

            else:
                if self.multipliers is not None:
                    if self.powers is not None:
                        return lambda n: self.get_ways_from_dels(n) + \
                                         self.get_ways_from_power(n)
                    else:
                        return lambda n: self.get_ways_from_dels(n)
                else:
                    if self.powers is not None:
                        return lambda n: self.get_ways_from_power(n)
                    else:
                        raise AttributeError("can't solve task if robot don't have any actions")


class CombSolverWithoutTr(CombSolver):
    def __init__(self, start: int, end: int, pluses=None, multipliers=None, powers=None, prev=False):
        super().__init__(start, end, pluses, multipliers, powers, prev)

    def get_ways_from_pluses(self, n):
        ways = 0


        for p in self.pluses:
            if n - p >= self.start:
                ways += self.all_ways[n - p - self.start]

        return ways

    def get_ways_from_dels(self, n):
        ways = 0
        for m in self.multipliers:
            if n % m == 0 and n // m >= self.start:
                ways += self.all_ways[n // m - self.start]
        return ways

    def get_ways_from_power(self, n):
        ways = 0
        for m in self.multipliers:
            x = n ** (1 / m)
            # if x exists in cache, it also will be integer
            if x in range(self.start, n + 1):
                ways += self.all_ways[int(x) - self.start]
        return ways

    # calculate number of ways for every number
    def get_comb_without_trajectory(self, debug=False):
        # count of methods to get this number
        for n in range(self.start + 1, self.end):
            self.all_ways[n - self.start] = self.calculate_f(n)

        print(f'Answer -  {self.all_ways[-1]} \n')

        # print table of ways if user want
        if debug:
            self.debug_log()


class CombSolverTr(CombSolver):
    """
    This class solve task with Trajectory Points and  not Trajectory Points
    :tr - points in trajectory

    :not_tr - points out of trajectory

    """

    def __init__(self, start: int, end: int, tr: [], not_tr: [], pluses=None, multipliers=None, powers=None, prev=False):
        super().__init__(start, end, pluses, multipliers, powers, prev)
        self.not_tr = not_tr
        self.tr = tr
        self.now_tr = start

    def get_ways_from_pluses(self, n):
        ways = 0
        for p in self.pluses:
            #  number must be more than trajectory and don't be in not_trajectory
            if (n - p >= self.now_tr) and (n - p not in self.not_tr):
                ways += self.all_ways[n - p - self.start]
        return ways

    def get_ways_from_dels(self, n):
        ways = 0
        for m in self.multipliers:

            #  number must be more than trajectory and don't be in not_trajectory
            if (n % m == 0) and \
                    (n / m >= self.now_tr) and \
                    (n // m not in self.not_tr):
                ways += self.all_ways[n // m - self.start]
        return ways

    def get_ways_from_power(self, n):
        ways = 0
        for m in self.multipliers:
            x = n ** (1 / m)
            #  number must be more than trajectory and don't be in not_trajectory
            if (x in range(self.now_tr, n + 1)) \
                    and (x not in self.not_tr):
                ways += self.all_ways[int(x) - self.start]

        return ways

    # calculate ways from
    # one trajectory point to another
    def fill_range(self, next_tr):
        for n in range(self.now_tr + 1, next_tr):
            self.all_ways[n - self.start] = self.calculate_f(n)

    # make all steps for one range between trajectory points
    def do_one_tr(self, tr):
        self.fill_range(tr)
        # calculate ways of trajectory point
        # !!! always do it BEFORE changing trajectory!
        self.all_ways[tr - self.start] = self.calculate_f(tr)
        self.now_tr = tr

    # split range of values to ranges and calculate ways for each
    def get_comb_with_trajectory(self, debug=False):
        # fill not trajectories with null
        for tr in self.not_tr:
            self.all_ways[tr - self.start] = 0

        if len(self.tr) == 0:
            self.fill_range(self.end)
        else:
            # start range always is (start, first trajectory)
            self.do_one_tr(self.tr[0])

            # main part
            for tr in range(1, len(self.tr)):
                self.do_one_tr(self.tr[tr])

            # last range always is (last trajectory; end)
            self.fill_range(self.end)

            # print numbers of ways to last number
        print(f'Answer -  {self.all_ways[-1]} \n')
        # print table if user want
        if debug:
            self.debug_log()


def main():
    # print('Task Without Trajectory')
    # # из 3 в 10 используя +1 +2, *2, сумма прведушего
    # c = CombSolverWithoutTr(3, 10, [1,3], [])
    # c = CombSolverWithoutTr(1, 55, [2], [3])
    # c = CombSolverWithoutTr(1, 55, [1,3],)
    # c.get_comb_without_trajectory(True)
    print()
    print('Task With Trajectory')

    start = 3
    end = 20
    tr = [15]
    not_tr = [10]
    plus = [1,3]
    p = []

    ct = CombSolverTr(start, end, tr, not_tr, pluses=plus,multipliers= p)
    # True - показывать таблицу
    ct.get_comb_with_trajectory(True)


if __name__ == '__main__':
    main()
