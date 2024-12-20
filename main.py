# This file simulates how overrepresented a state would be in the american electoral college.
# Parameters:
# * The population of each state
# * The total number of electors (in america, it's 538)
# * The base number of electors each state starts with (in america, it's 3)
#
# The algorithm is called the "method of equal proportions"
# https://www.census.gov/newsroom/blogs/random-samplings/2021/04/how-apportionment-is-calculated.html
# https://en.wikipedia.org/wiki/Huntington%E2%80%93Hill_method
#
# How the algorithm works:
# * All states are given the base number of electors
# * For each remaining elector:
#   * calculate the priority of each state.
#   * if E is the number of current electors for a state and P is the
#     population of the state, then a state's priority is P / (E * (E + 1))
#   * the state with the highest priority gets this iteration's elector.

from math import sqrt

def priority(population, current_electors):
    e = current_electors + 1
    return population / sqrt(e * (e + 1))

def calculate_electors(populations: list[int], num_electors=100, base_state_electors=3):
    n = len(populations)
    assert(num_electors >=n * base_state_electors)

    electors = [base_state_electors] * n
    for _ in range(num_electors - base_state_electors * n):
        priorities = [priority(populations[i], electors[i]) for i in range(n)]
        max_prio_i = -1
        max_prio = 0
        for i, p in enumerate(priorities):
            if p > max_prio:
                max_prio_i = i
                max_prio = p
        electors[max_prio_i] += 1
    return electors

# populations and electors are both lists of integers.
# this will return two lists of strings such that each field lines up with the
# others in clean columns.
def column_align(populations: list[int], electors: list[int]):
    n = len(populations)
    assert(n == len(electors))
    aligned_populations = [""] * n
    aligned_electors = [""] * n
    for i, (p, e) in enumerate(zip(populations, electors)):
        width = max(len(str(p)), len(str(e)))
        aligned_populations[i] = f"{p:{width}}"
        aligned_electors[i] = f"{e:{width}}"
    return aligned_populations, aligned_electors

def summarize(populations, ne, be):
    total_pop = sum(populations)

    electors = calculate_electors(populations, ne, be)
    total_electors = sum(electors)

    print(f"{ne} electors, every state has at least {be}")
    aligned_populations, aligned_electors = column_align(populations, electors)
    print("state populations:", aligned_populations)
    print("state electors:   ", aligned_electors)
    for i in range(len(populations)):
        pop_frac = populations[i] / total_pop
        ele_frac = electors[i] / total_electors
        overrep_factor = ele_frac / pop_frac
        print(
            f"state {i} is overrepresented by {overrep_factor:5.4f}" +
            f"({pop_frac:5.4f} of the population and {ele_frac:5.4f} of the electors)"
        )
    print()

populations = [1, 10, 100, 500]
for ne, be in [(100, 0), (100, 1), (100, 2), (100, 3)]:
    summarize(populations, ne, be)

for ne, be in [(100, 0), (1000, 0), (10000, 0), (100000, 0)]:
    summarize(populations, ne, be)

# Output:

# 100 electors, every state has at least 0
# state populations: ['1', '10', '100', '500']
# state electors:    ['0', ' 1', ' 16', ' 83']
# state 0 is overrepresented by 0.0000(0.0016 of the population and 0.0000 of the electors)
# state 1 is overrepresented by 0.6110(0.0164 of the population and 0.0100 of the electors)
# state 2 is overrepresented by 0.9776(0.1637 of the population and 0.1600 of the electors)
# state 3 is overrepresented by 1.0143(0.8183 of the population and 0.8300 of the electors)
#
# 100 electors, every state has at least 1
# state populations: ['1', '10', '100', '500']
# state electors:    ['1', ' 1', ' 16', ' 82']
# state 0 is overrepresented by 6.1100(0.0016 of the population and 0.0100 of the electors)
# state 1 is overrepresented by 0.6110(0.0164 of the population and 0.0100 of the electors)
# state 2 is overrepresented by 0.9776(0.1637 of the population and 0.1600 of the electors)
# state 3 is overrepresented by 1.0020(0.8183 of the population and 0.8200 of the electors)
#
# 100 electors, every state has at least 2
# state populations: ['1', '10', '100', '500']
# state electors:    ['2', ' 2', ' 15', ' 81']
# state 0 is overrepresented by 12.2200(0.0016 of the population and 0.0200 of the electors)
# state 1 is overrepresented by 1.2220(0.0164 of the population and 0.0200 of the electors)
# state 2 is overrepresented by 0.9165(0.1637 of the population and 0.1500 of the electors)
# state 3 is overrepresented by 0.9898(0.8183 of the population and 0.8100 of the electors)
#
# 100 electors, every state has at least 3
# state populations: ['1', '10', '100', '500']
# state electors:    ['3', ' 3', ' 15', ' 79']
# state 0 is overrepresented by 18.3300(0.0016 of the population and 0.0300 of the electors)
# state 1 is overrepresented by 1.8330(0.0164 of the population and 0.0300 of the electors)
# state 2 is overrepresented by 0.9165(0.1637 of the population and 0.1500 of the electors)
# state 3 is overrepresented by 0.9654(0.8183 of the population and 0.7900 of the electors)
#
# 100 electors, every state has at least 0
# state populations: ['1', '10', '100', '500']
# state electors:    ['0', ' 1', ' 16', ' 83']
# state 0 is overrepresented by 0.0000(0.0016 of the population and 0.0000 of the electors)
# state 1 is overrepresented by 0.6110(0.0164 of the population and 0.0100 of the electors)
# state 2 is overrepresented by 0.9776(0.1637 of the population and 0.1600 of the electors)
# state 3 is overrepresented by 1.0143(0.8183 of the population and 0.8300 of the electors)
#
# 1000 electors, every state has at least 0
# state populations: ['1', '10', '100', '500']
# state electors:    ['1', '15', '163', '821']
# state 0 is overrepresented by 0.6110(0.0016 of the population and 0.0010 of the electors)
# state 1 is overrepresented by 0.9165(0.0164 of the population and 0.0150 of the electors)
# state 2 is overrepresented by 0.9959(0.1637 of the population and 0.1630 of the electors)
# state 3 is overrepresented by 1.0033(0.8183 of the population and 0.8210 of the electors)
#
# 10000 electors, every state has at least 0
# state populations: [' 1', ' 10', ' 100', ' 500']
# state electors:    ['15', '163', '1636', '8186']
# state 0 is overrepresented by 0.9165(0.0016 of the population and 0.0015 of the electors)
# state 1 is overrepresented by 0.9959(0.0164 of the population and 0.0163 of the electors)
# state 2 is overrepresented by 0.9996(0.1637 of the population and 0.1636 of the electors)
# state 3 is overrepresented by 1.0003(0.8183 of the population and 0.8186 of the electors)
#
# 100000 electors, every state has at least 0
# state populations: ['  1', '  10', '  100', '  500']
# state electors:    ['163', '1636', '16366', '81835']
# state 0 is overrepresented by 0.9959(0.0016 of the population and 0.0016 of the electors)
# state 1 is overrepresented by 0.9996(0.0164 of the population and 0.0164 of the electors)
# state 2 is overrepresented by 1.0000(0.1637 of the population and 0.1637 of the electors)
# state 3 is overrepresented by 1.0000(0.8183 of the population and 0.8184 of the electors)


# Conclusion:
# while the priority is calculated using a denominator that increases
# superlinearly, in practice it is only barely superlinear. It might as well be
# linear. The real impact on overrepresentation of smaller states is how many
# base electors there are. In the american electoral system, there are 3 base
# electors.
