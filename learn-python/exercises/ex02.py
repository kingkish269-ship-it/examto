# Module 1 - Lesson 2: String methods (.split)
# Read lessons/02_strings.md. Replace BLANK. Then: python3 check.py 2
def get_username(line):
    # line looks like: "FAILED login user=admin"
    # 1) split into words, take the last word -> "user=admin"
    # 2) split that on "=" and take the part after it -> "admin"
    last_word = line.split()[-1]          # "user=admin"
    return last_word.split("=")[BLANK]    # BLANK -> 1
