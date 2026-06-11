# -*- coding: utf-8 -*-
import subprocess
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

def run_git(args):
    try:
        res = subprocess.run(["git"] + args, cwd=workspace_dir, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        return res.stdout, res.stderr
    except Exception as e:
        return "", str(e)

out_file = os.path.join(workspace_dir, "scratch", "git_search_res.txt")
with open(out_file, "w", encoding="utf-8") as out:
    out.write("=== GIT LOG -S switchNtbRegion ===\n")
    stdout, stderr = run_git(["log", "-S", "switchNtbRegion", "--oneline"])
    out.write("STDOUT:\n" + stdout + "\nSTDERR:\n" + stderr + "\n\n")

    out.write("=== GIT LOG -S renderNtbAnalysisTable ===\n")
    stdout, stderr = run_git(["log", "-S", "renderNtbAnalysisTable", "--oneline"])
    out.write("STDOUT:\n" + stdout + "\nSTDERR:\n" + stderr + "\n\n")

    out.write("=== GIT STATUS ===\n")
    stdout, stderr = run_git(["status"])
    out.write("STDOUT:\n" + stdout + "\nSTDERR:\n" + stderr + "\n\n")

    out.write("=== GIT LOG LATEST COMMITS ===\n")
    stdout, stderr = run_git(["log", "-n", "20", "--oneline"])
    out.write("STDOUT:\n" + stdout + "\nSTDERR:\n" + stderr + "\n\n")

print("Saved git search results to git_search_res.txt")
