# Access token for your GroupMe acc.    (CHANGE THIS)
ACCESS_TOKEN = '0000000000000000000000000000000000000000'

# GroupMe API URL
GROUPME_API_URL = "https://api.groupme.com/v3"

# Query
QUERY = GROUPME_API_URL + "/groups?omit='memberships'&token=%s" % ACCESS_TOKEN

# For at_all function
is_before_mention = True
message = "Hi everyone lmao!"
