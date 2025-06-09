#!/usr/bin/env python3
"""
Script to update job experience format in CV HTML files
Changes from:
<div class="job-header">
    <div class="job-title">- Job Title</div>
    <div class="company">Company Name</div>
    <div class="date">Date Range</div>
</div>

To:
<div class="job-title-line">- Job Title | Date Range</div>
<div class="company-indented">Company Name</div>
"""

import re
import sys


def update_job_format(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern to match the old job header format
    pattern = r'<div class="job-header">\s*<div class="job-title">(.*?)</div>\s*<div class="company">(.*?)</div>\s*<div class="date">(.*?)</div>\s*</div>'

    def replace_job_header(match):
        job_title = match.group(1).strip()
        company = match.group(2).strip()
        date = match.group(3).strip()

        return f'<div class="job-title-line">{job_title} | {date}</div>\n        <div class="company-indented">{company}</div>'

    # Replace all occurrences
    updated_content = re.sub(pattern, replace_job_header, content, flags=re.DOTALL)

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"Updated job format in {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_job_format.py <html_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    update_job_format(file_path)
