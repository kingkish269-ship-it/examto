# Module 3 - Lesson 12: Error handling (try/except)
# Read lessons/12_errors.md. Replace BLANK. Then: python3 check.py 12
def safe_int(value, default=0):
    # Convert value to an int. If it is not a valid number, return default.
    try:
        return int(value)
    except ValueError:
        return BLANK                      # BLANK -> default
