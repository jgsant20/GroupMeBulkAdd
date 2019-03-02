from functions import *
from constants import *

import sys


def run():
    """Run this if you're not sure of the GroupID or the CSV file name"""
    list_of_groups = get_all_groups(QUERY)
    list_of_csvfiles = get_all_csvfiles()
    group_info = choose_group(list_of_groups)
    group_id = group_info[1]
    roster = choose_roster(list_of_csvfiles)

    while True:
        print("The numbers within '{}' will be added to {}".format(roster, group_info))

        if input('Please Confirm (y/n): ') == 'y':
            break

        sys.exit(1)

    add_members(group_id, roster)


def quick_run(group_id, roster):
    try:
        add_members(group_id, roster)
        print("Successfully added members in '{}' to {}".format(roster, group_id))
    except Exception as e:
        print("{}: Members from '{}' unsuccessfully added to {}".format(e, roster, group_id))


def bulk_run():
    for group_id, roster in DATA:
        quick_run(group_id, roster)


if __name__ == '__main__':
    run()
