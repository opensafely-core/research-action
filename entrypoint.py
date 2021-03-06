import os
from pathlib import Path
import subprocess
import sys
import zipfile

import requests
from github import Github


# Get URL of archive of git repo using API.
github = Github(os.environ["GITHUB_TOKEN"])
repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
print(f"Using GITHUB_REF: {os.environ['GITHUB_REF']}")
archive_url = repo.get_archive_link("zipball", os.environ["GITHUB_REF"])

# Download and unzip archive.
rsp = requests.get(archive_url, stream=True)
if not rsp.ok or "content-disposition" not in rsp.headers:
    print(rsp)
    sys.exit(f"Could not download {archive_url}")

filename = rsp.headers["content-disposition"].split("filename=")[1]

with open(filename, "wb") as f:
    for chunk in rsp.iter_content(32 * 1024):
        f.write(chunk)

with zipfile.ZipFile(filename) as f:
    f.extractall()

    # The zipfile should contain a single directory.
    dirname = f.namelist()[0]
    assert all(name.startswith(dirname) for name in f.namelist())


cmds = []

codelists = Path(dirname) / 'codelists'
if codelists.exists():
    cmds.append(("Checking codelists", ["opensafely", "codelists", "check"]))
else:
    print("No codelists directory - skipping codelists tests")

cmds.append(
    ("Running the project", ["opensafely", "run", "run_all", "--continue-on-error", "--timestamps"]),
)

for step_name, cmd in cmds:
    # Run each test command in turn.  We depend on the commands producing useful output,
    # and returning non-zero if they have failed.
    print("=" * 80)
    print(f">>> {step_name}")
    print()
    rv = subprocess.run(cmd, cwd=dirname, env=os.environ)
    if rv.returncode != 0:
        sys.exit(1)
