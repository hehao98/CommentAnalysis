# Comment Analysis on World of Code

This folder contains source code and dataset for a comment analysis study based on the [World of Code](https://github.com/ssc-oscar) Dataset (Or OSCAR). Most of the scripts in this folder must be run on the World of Code server to access the needed raw data.

This folder is still under active development, so do not expect it to work right.

## Dependencies

### Oscar.py

[Oscar.py](https://github.com/ssc-oscar/oscar.py) is a convenience python library to access the World of Code dataset. To install:

```
# pip is not available on OSCAR servers
easy_install --user --upgrade oscar
```

## The data processing workflow

project_names->project_urls->filtered_project_urls->trees_and_files