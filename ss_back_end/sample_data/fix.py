"""
When we use chatGPT prompts to generate sample data, we might not want to waste
context tokens on IDs. Use this script to generate some
"""
import csv

new_str = ''

with open('financial_compliance_feedback_database.csv.orig', newline='') as csvfile:
    template = "FCITEM-"
    the_id = 1
    rows = csvfile.read().split("\n")
    new_str += '"ID","TITLE","DESCRIPTION"\n'
    for row in rows[1:]:
        row = f'"{template}{the_id}",{row}\n'
        new_str += row
        the_id += 1
    print(new_str)
