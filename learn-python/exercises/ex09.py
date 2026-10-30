# Module 2 - Lesson 9: Regex (pull an IP out of text)
# Read lessons/09_regex.md. Replace BLANK. Then: python3 check.py 9
import re
def extract_ip(text):
    # find the first IPv4 address in the text and return it
    match = re.search(r"(\d+\.\d+\.\d+\.\d+)", text)
    return match.group(BLANK)             # BLANK -> 1
