'''
Run Python profiler to analyze Pelican performance

All commandline arguments (sys.argv) are passed on to Pelican
'''

import cProfile
import pelican
import sys

PROFILE_RESULTS = 'profile_output.txt'
SORT_BY = 'tottime'  # https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats


def main():
    stdout = sys.stdout
    with open(PROFILE_RESULTS, 'w') as result:
        sys.stdout = result
        cProfile.run(
            'pelican.main()',
            sort=SORT_BY
        )
        sys.stdout = stdout


if __name__ == '__main__':
    main()
