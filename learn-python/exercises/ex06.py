# Module 2 - Lesson 6: Loops + conditions (filtering)
# Read lessons/06_filtering.md. Replace BLANK. Then: python3 check.py 6
def high_findings(findings):
    result = []
    for f in findings:
        if f["severity"] == BLANK:        # BLANK -> "HIGH"
            result.append(f)
    return result
