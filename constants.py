# Access token for your GroupMe acc.    (CHANGE THIS)
ACCESS_TOKEN = '0000000000000000000000000000000000000000'

# GroupMe API URL
GROUPME_API_URL = "https://api.groupme.com/v3"

# Query
QUERY = GROUPME_API_URL + "/groups?omit='memberships'&token=%s" % ACCESS_TOKEN


# ==============================================================
# Constants below used for quick access if group_id and rosters are already known.

# GroupMe group ID
GROUP_ID = ''

# CSV file that contains all numbers
ROSTER = 'csv.txt'

# Contains list of tuples(group_id, roster)

"""
DATA = [(47750320, 'csv/Setup.csv'),
        (47750380, 'csv/First Shift.csv'),
        (47750384, 'csv/Ongoing.csv'),
        (47750391, 'csv/I.Ongoing.csv'),
        (47750395, 'csv/Last Shift.csv'),
        (47750400, 'csv/Cleanup.csv'),
        ]
"""

DATA = [(47902602, 'csv/test.csv')]
