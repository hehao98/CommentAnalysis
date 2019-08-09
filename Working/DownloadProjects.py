"""
Download projects from a project csv file and put them in [output_path]/projects
"""

import pandas as pd
import subprocess
import os
import argparse
from datetime import datetime
from multiprocessing import Pool
from termcolor import colored


def remove_non_code_files(path):
    """
    Remove non-code files in the project dataset larger than 64KB,
        to save storage space
    """
    for root, dirs, files in os.walk(path):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            try:
                full_path = os.path.join(root, file)
                if file.endswith(".java") or file.endswith(".py") or file.endswith(".txt") or file.endswith(".md"):
                    continue
                if os.path.getsize(full_path) <= 64*1024:
                    continue
                os.remove(full_path)
                print("Removed", full_path)
            except FileNotFoundError:
                print(colored("FileNotFoundError: {}".format(full_path), "red"))


def run_proc(index, url, name):
    print(colored("Downloading Project {}...".format(index), "green"))
    subprocess.call(
        "git clone {}.git {}".format(url, name), shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csv_path", help="Path to the CSV file storing project information")
    parser.add_argument(
        "output_path", help="Path where the downloaded projects will be stored")
    parser.add_argument("-j", type=int, default=4,
                        help="Number of Jobs (Default 4)")
    args = vars(parser.parse_args())
    csv_path = args["csv_path"]
    output_path = args["output_path"]
    num_job = args["j"]

    begin_time = datetime.now()

    projects = pd.read_csv(csv_path)
    os.chdir(output_path)
    if not os.path.exists("projects/"):
        os.mkdir("projects")
    os.chdir("projects")

    pool = Pool(num_job)
    for index, row in projects.iterrows():
        if os.path.exists(os.path.join(output_path, "/projects/{}".format(row["name"]))):
            print(colored("Skipping {} because the folder already exists...", "yellow"))
            continue
        pool.apply_async(run_proc, args=(index, row["url"], row["name"]))
    pool.close()
    pool.join()

    print(colored("Start Cleanning Files...", "yellow"))

    remove_non_code_files(".")

    print("Total running time: {}".format(datetime.now() - begin_time))
