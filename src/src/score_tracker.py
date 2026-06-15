import re


def extract_score(feedback):

    match = re.search(r'(\d+)/10', feedback)

    if match:
        return int(match.group(1))

    return 0
