"""Decide which services need testing from a list of changed files.

  services/<name>/...        -> that service
  shared/, scripts/, .github/workflows/ci.yml -> every service (they affect all of them)
  anything else (README, docs) -> nothing
Prints a JSON object for a GitHub Actions matrix: {"service": [...]}.
"""
import json
import os
import subprocess
import sys

EVERYTHING = ("shared/", "scripts/", ".github/workflows/ci.yml")


def all_services(root="services"):
    return sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))


def changed_services(files, services):
    hit = set()
    for f in files:
        if f.startswith(EVERYTHING):
            return sorted(services)
        parts = f.split("/")
        if parts[0] == "services" and len(parts) > 2 and parts[1] in services:
            hit.add(parts[1])
    return sorted(hit)


def main(base, head):
    services = all_services()
    if not base or set(base) == {"0"}:          # first push on a branch: no base to compare to
        files = ["shared/x"]
    else:
        files = subprocess.check_output(["git", "diff", "--name-only", base, head], text=True).split()
    print(json.dumps({"service": changed_services(files, services)}))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "", sys.argv[2] if len(sys.argv) > 2 else "HEAD")
