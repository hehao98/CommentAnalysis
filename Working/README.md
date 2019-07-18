# Comment Analysis on World of Code

This folder contains source code and dataset for a comment analysis study based on the [World of Code](https://github.com/ssc-oscar) Dataset (Or OSCAR). Most of the scripts in this folder must be run on the World of Code server to access the needed raw data.

This folder is still under active development, so do not expect it to work right.

## Dependencies

### Oscar.py

[Oscar.py](https://github.com/ssc-oscar/oscar.py) is a convenience python library to access the World of Code dataset. To install:

```
# pip is not available on OSCAR servers
easy_install --user --upgrade oscar lzf tokyocabinet fnvhash
```

## The data processing workflow

### Retrieve, Filter and Build Project Data

Execute the python scripts in order on WoC da4.

```
python RetrieveProjectList.py
python GenerateGHTorrentDB.py
python FilterProjects.py
python DownloadProjectMetadata.py [GitHub Username] [GitHub Access Token]
python BuildProjectCSV.py
```

### Setup Server over SSH Tunneling

```
ssh -L 23333:da4.eecs.utk.edu:23333 heh@da4.eecs.utk.edu -i ~/.ssh/worldofcode -p 443 -o ServerAliveInterval=60
# In remote bash
cd CommentAnalysis/Working
export FLASK_APP=Server.py
python -m flask run -p 23333 --host=0.0.0.0
```

### Do the Analysis

```
python CountLineOfCode.py
```