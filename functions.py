from constants import *

import requests
import csv
import json
import glob
import sys


def get_group_query(group_id):
    return GROUPME_API_URL + "/groups/" + str(group_id) + "/members/add" +\
           "?token=" + ACCESS_TOKEN


def format_numbers(number):
    all_numbers = [str(i) for i in range(10)]
    return ''.join([str(n) for n in number if str(n) in all_numbers])


def csv_to_json(roster):
    with open(roster, 'rt') as csvfile:
        members = list(csv.reader(csvfile))[0]
        members_data = []

        for member in members:

            if member == '':
                continue

            number = format_numbers(member)
            new_groupme_member = {'phone_number': number}
            members_data.append(new_groupme_member)

    wrapper = {'members': members_data}
    json_members = json.dumps(wrapper)
    return json_members


def add_members(group_id, roster):
    json_members = csv_to_json(roster)
    query = get_group_query(group_id)
    requests.post(query, data=json_members)


def get_all_groups(query):
    list_of_groupid_names = []
    json_groups = requests.get(query).json()["response"]
    for group in json_groups:
        list_of_groupid_names.append((group["name"], group["group_id"]))
    return list_of_groupid_names


def choose_group(list_of_groups):
    for i, (name, id) in enumerate(list_of_groups):
        print("[{}]: {}, '{}'".format(i, id, name))

    choice = int(input('\nChoose Group to bulk add members to (index): '))
    while not (0 <= choice < len(list_of_groups)):
        choice = int(input('Choose an input from (0 - {}): '.format(len(list_of_groups)-1)))

    print('\n')
    group_info = list_of_groups[choice]
    return group_info


def get_all_csvfiles():
    list_of_csvfiles = [file for file in glob.glob('csv/*.csv')]
    return list_of_csvfiles


def choose_roster(list_of_csvfiles):
    for i, name in enumerate(list_of_csvfiles):
        print("[{}]: {}".format(i, name))

    choice = int(input('\nChoose csv file to add to group (index): '))
    while not (0 <= choice < len(list_of_csvfiles)):
        choice = int(input('Choose an input from (0 - {}): '.format(len(list_of_csvfiles)-1)))

        if choice == -1:
            sys.exit(1)

    print('\n')
    csv_name = list_of_csvfiles[choice]
    return csv_name
