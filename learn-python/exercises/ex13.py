# Module 4 - Lesson 13: Build a command-line tool (argparse)
# Read lessons/13_cli.md. Replace BLANK. Then: python3 check.py 13
import argparse
def build_parser():
    parser = argparse.ArgumentParser(description="Filter findings")
    parser.add_argument("file")                       # required input file
    parser.add_argument("--severity", default=BLANK)  # BLANK -> "HIGH"
    return parser
