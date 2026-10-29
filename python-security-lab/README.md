# Python Security Lab

This lab teaches the Python needed for cloud security, security automation, and DevSecOps roles. It does not try to turn you into an application developer.

## Automatic shadow-coding mode

All eight examples are already implemented and tested. You do not need to start from a blank file or remember syntax. Run the complete demonstration with:

```bash
python3 run_demo.py
```

The demonstration parses findings, filters risks, simulates a paginated API, writes a report, retries a temporary failure, runs a CLI workflow, and audits cloud security groups.

Use this learning loop:

1. Run one working example.
2. Read ten to twenty lines of its code.
3. Explain what security decision the code makes.
4. Ask Kiro to make one small change and show the difference.
5. Re-run the tests automatically.

This removes blank-page coding. Your target is to understand, review, and safely modify scripts, not memorize punctuation.

## Your finish line

You are ready when you can recognize and adapt these eight patterns:

1. Parse JSON from a security tool.
2. Read nested dictionaries safely.
3. Filter findings with business rules.
4. Call a paginated API.
5. Write a CSV report.
6. Handle failures and retry safely.
7. Turn a script into a command-line tool.
8. Combine the patterns into a cloud-security audit.

You do **not** need LeetCode, advanced algorithms, web frameworks, metaclasses, decorators, or syntax memorization for this learning phase.

## Learning method

Work for 20–30 minutes, four days each week. Kiro handles file editing and test execution.

For each drill:

1. Read the short working function.
2. Run its test and demonstration.
3. Explain the input, security decision, and output in plain language.
4. Ask Kiro to change one rule, such as changing a severity threshold or adding a risky port.
5. Compare the old and new test output.
6. Use `CHEATSHEET.md` whenever syntax is unfamiliar.
7. Revisit the same pattern seven days later.

You are never required to type a complete program from memory. You must eventually be able to explain working code and recognize an unsafe change, because interviews and production reviews cannot be automated on your behalf.

## Requirements

- Python 3.10 or newer
- No paid service
- No external Python package for these drills
- No AWS account for the first eight drills

Check Python:

```bash
python3 --version
```

## Run one drill

Start with Drill 1 only:

```bash
cd python-security-lab
python3 -m unittest tests.test_01_parse_findings -v
```

The drill is already implemented. The test shows the expected behavior and gives immediate feedback after any future modification.

Verify the complete lab:

```bash
USE_SOLUTIONS=1 python3 -m unittest discover -v
```

Run all working examples when you want a full check. On learning days, focus on one drill even though the full lab is already green.

## Four-week schedule

### Week 1: Security data

- Day 1: Run Drill 1 and explain how severity counts are produced.
- Day 2: Run Drill 2 and find where missing keys are handled.
- Day 3: Run Drill 3 and ask Kiro to change the minimum severity.
- Day 4: Review the three outputs without modifying code.

### Week 2: Automation mechanics

- Day 1: Run Drill 4 and trace the two API pages.
- Day 2: Run Drill 5 and inspect the generated CSV.
- Day 3: Run Drill 6 and compare retryable and non-retryable errors.
- Day 4: Ask Kiro to add one test, then review why it passes.

### Week 3: Reusable tools

- Day 1: Run Drill 7 with HIGH and CRITICAL thresholds.
- Day 2: Ask Kiro to add a `--status` option and explain the change.
- Day 3: Run Drill 8 and map every finding to its source rule.
- Day 4: Ask Kiro to add one risky port that you choose.

### Week 4: Retention and interview proof

- Explain Drills 4, 6, and 8 without reading their documentation.
- Review one intentionally unsafe code change and identify the risk.
- Describe the threat model, inputs, decisions, and output in your own words.
- Practice a five-minute screen-share walkthrough of the security-group auditor.

## What each drill proves in an interview

| Drill | Job skill |
|---|---|
| 1–3 | Read SAST, CSPM, SIEM, and cloud API output |
| 4 | Integrate security products through REST APIs |
| 5 | Produce evidence for engineers and auditors |
| 6 | Write automation that survives transient failures |
| 7 | Package a script so another engineer can use it |
| 8 | Turn cloud-security knowledge into executable checks |

## After this lab

Only after these drills are comfortable, move to:

1. `requests` and authenticated REST APIs.
2. `boto3` read-only AWS inventory.
3. `pytest` and mocking.
4. GitHub Actions YAML.
5. Semgrep, Trivy, Gitleaks, Checkov, and OWASP ZAP integration.
6. Terraform basics and policy-as-code.

The next portfolio project should be an AWS exposure auditor built from Drill 8. Do not start ten tools at once.
