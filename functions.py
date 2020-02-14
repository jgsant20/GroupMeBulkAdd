from constants import *

import requests
import csv
import json
import glob
import sys


def get_group_add_query(group_id):
    return GROUPME_API_URL + "/groups/" + str(group_id) + "/members/add" + \
           "?token=" + ACCESS_TOKEN


def get_group_send_query(group_id):
    return GROUPME_API_URL + "/groups/" + str(group_id) + "/messages" +\
           "?token=" + ACCESS_TOKEN


def is_phone_number(number):
    return len(format_phone_numbers(number)) >= 9


def is_email(email):
    return '@' in email


def format_phone_numbers(number):
    all_numbers = [str(i) for i in range(10)]
    return ''.join([str(n) for n in number if str(n) in all_numbers])


# Returns an object of the following structure:
#   {'members': ['email': xx, 'email': xx, 'phone_number': xx, ...]}
def csv_to_json(roster):
    """ Converts data from roster to an exportable json object
    :param roster: [String] Directory to csv file
    :return: [json] Exportable json object for posting to add_query
    """
    with open(roster, 'rt') as csvfile:
        members = list(csv.reader(csvfile))[0]
        members_data = []

        for member in members:
            if member == '':
                continue

            if is_phone_number(member):
                number = format_phone_numbers(member)
                new_groupme_member = {'phone_number': number}
                members_data.append(new_groupme_member)
            elif is_email(member):
                new_groupme_member = {'email': member}
                members_data.append(new_groupme_member)

    wrapper = {'members': members_data}
    json_members = json.dumps(wrapper)
    return json_members


def get_all_groups(query):
    """ Queries GroupMe server for data and returns a list of group information
    :param query: [String] Query link
    :return: [List] Returns list of groups and their associated data
    """
    list_of_groups = []
    json_groups = requests.get(query).json()["response"]
    return json_groups


def choose_group(list_of_groups):
    for i in range(len(list_of_groups)):
        print("[{}]: {}, '{}'".format(i, list_of_groups[i]["group_id"], list_of_groups[i]["name"]))

    choice = int(input('\nChoose Group to run functions with: '))
    while not (0 <= choice < len(list_of_groups)):
        choice = int(input('Choose an input from (0 - {}): '.format(len(list_of_groups) - 1)))

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
        choice = int(input('Choose an input from (0 - {}): '.format(len(list_of_csvfiles) - 1)))

        if choice == -1:
            sys.exit(1)

    print('\n')
    csv_name = list_of_csvfiles[choice]
    return csv_name


""" GroupMe functions are written below.
"""


#   {'message': ['attachments': ['type':'mentions', ]]}
def add_members(group_id, roster):
    """ Adds members from roster to unique GroupMe group determined by 'group_id'
    :param group_id: [int] Unique group id
    :param roster: [String] Directory to csv file
    """
    json_members = csv_to_json(roster)
    query = get_group_add_query(group_id)
    requests.post(query, data=json_members)


def at_all(group_id, group_members, message_to_send, is_before_mentions=True):
    """ Mentions everyone within a group and sends a message at the end
    :param group_id: [int] Unique group id
    :param group_members: [List] List of group members within group from unique group id
    :param message_to_send: [String] Message to send
    :param is_before_mentions: [bool] If true, message will be sent before mentions. Else, message will be sent after.
    """

    query = get_group_send_query(group_id)
    user_ids = []
    loci = []
    text = ''
    msg_len = 0

    if len(message_to_send) != 0 and is_before_mentions:
        text += message_to_send + ' '
        msg_len += len(message_to_send) + 1

    for m in group_members:
        text += '@' + m['nickname'] + ' '
        loci.append([msg_len, len(m['nickname']) + 1])
        msg_len += len(m['nickname']) + 2
        user_ids.append(m['user_id'])

        # Sends a message before character limit (1000) is reached
        if msg_len >= 950:
            requests.post(query, json={
                "message": {"text": text, "attachments": [{'loci': loci, 'type': 'mentions', 'user_ids': user_ids}]}})
            user_ids = []
            loci = []
            text = ''
            msg_len = 0

    # We do this in-case the file in case there are remaining members to be mentioned after all members are read
    if msg_len < 950:
        data = {"message": {"text": text, "attachments": [{'loci': loci, 'type': 'mentions', 'user_ids': user_ids}]}}
        requests.post(query, json=data)

    if len(message_to_send) != 0 and not is_before_mentions:
        data = {"message": {"text": message_to_send}}
        requests.post(query, json=data)
