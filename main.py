#!/usr/bin/env python3
from copy import deepcopy
from timeit import Timer
import sorters
from collections import namedtuple

Result = namedtuple('Result', ( 'sorter', 'seconds' ))
FileInfo = namedtuple('FileInfo', ( 'filename', 'datatype', 'numtimes' ))

SOURCE_FILES = [
    FileInfo( 'list0.txt', int,   100000 ),
    FileInfo( 'list1.txt', int,   100000 ),
    FileInfo( 'list2.txt', int,   100000 ),
    FileInfo( 'list3.txt', int,   100    ),
    FileInfo( 'list4.txt', int,   100000 ),
    FileInfo( 'list5.txt', float, 100000 ),
]

SORTERS = [
    sorters.bubble_sort,
    sorters.insertion_sort,
    sorters.selection_sort,
    sorters.quick_sort,
    sorters.python_sort,
]


def run_sort(func, lst):
    '''Arapper around a sort function to match the API of the Timer'''
    def inner():
        return func(lst, 0)
    return inner


def main():
    # read the lists from files
    master_lsts = []
    for fi in SOURCE_FILES:
        with open(fi.filename) as fin:
            lst = []
            for line in fin:
                lst.append([ fi.datatype(line.strip()) ])
            master_lsts.append(lst)

    # extend list3 significantly so we have a really long list
    lst3 = deepcopy(master_lsts[3])
    master_lsts[3] = []
    for i in range(500):
        master_lsts[3].extend([ [row[0]+i] for row in lst3 ])

    # time it with all the sorts
    for i, lst in enumerate(master_lsts):
        print('LIST {}: {} records'.format(i, len(lst)))
        results = []
        for sortfunc in SORTERS:
            clone = deepcopy(lst)
            t = Timer(run_sort(sortfunc, clone))
            results.append(Result(
                sortfunc.__name__,
                t.timeit(SOURCE_FILES[i].numtimes),
            ))

        # show the results for this list
        results.sort(key=lambda r: r[1])
        for result in results:
            print('\t{}: {} [{} more than {}]'.format(
                result.sorter,
                round(result.seconds, 3),
                round(result.seconds - results[0].seconds, 3),
                results[0].sorter,
            ))



### Main runner ###
if __name__ == '__main__':
    main()
