

def convert_messages(messages):  # convert list of dict to list
    ans = list()
    for d in messages:
        ans.append(d["message"])
    return ans
