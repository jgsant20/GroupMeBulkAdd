from functions import *
from constants import *

import sys


def run():
    """Run this if you're not sure of the GroupID or the CSV file name"""

    print("Choose what you want to do?\n"
          "[0]: Read CSV file of contact information to add to a group in GroupMe.\n"
          "[1]: Mention everyone in a group.")

    choice = int(input("Choose function to run: "))
    while not (0 <= choice < 2):
        choice = int(input('Choose an input from (0 - {}): '.format(1)))
    print("\n")

    list_of_groups = get_all_groups(QUERY)
    group_info = choose_group(list_of_groups)
    group_id = group_info["group_id"]
    group_members = group_info["members"]

    # BulkAdd
    if choice == 0:
        list_of_csvfiles = get_all_csvfiles()
        roster = choose_roster(list_of_csvfiles)

        while True:
            print("The numbers within '{}' will be added to {}".format(roster, group_info))

            if input('Please Confirm (y/n): ') == 'y':
                add_members(group_id, roster)
                break
            else:
                sys.exit(1)

    # Mention everyone in a group
    elif choice == 1:
        at_all(group_id, group_members, "testo")

    # Just exit lol
    else:
        print("aborting...")
        sys.exit(1)


if __name__ == '__main__':
    run()
