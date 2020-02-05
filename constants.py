# Access token for your GroupMe acc.    (CHANGE THIS)
ACCESS_TOKEN = '0000000000000000000000000000000000000000'

# GroupMe API URL
GROUPME_API_URL = "https://api.groupme.com/v3"

# Query
QUERY = GROUPME_API_URL + "/groups?omit='memberships'&token=%s" % ACCESS_TOKEN


# ==============================================================
# Constants below used for quick access if group_id and rosters are already known.
# FOR QUICK_RUN

# GroupMe group ID
GROUP_ID = ''

# CSV file that contains all numbers
ROSTER = 'csv/test.txt'


# ==============================================================
# Constants below used for quick access if group_id and rosters are already known.
# FOR BULK_RUN

# Contains list of tuples(group_id, roster)
DATA = [(00000000, 'csv/test.csv')]
