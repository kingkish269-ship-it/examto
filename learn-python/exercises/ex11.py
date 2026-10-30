# Module 3 - Lesson 11: Read a file
# Read lessons/11_files.md. Replace BLANK. Then: python3 check.py 11
def count_alerts(path):
    # Each non-empty line in the file is one alert. Return how many there are.
    with open(path) as file:
        lines = file.readlines()
    non_empty = [line for line in lines if line.strip()]
    return BLANK(non_empty)               # BLANK -> len
