# ESEC/FSE19-SRC

Source Code and Data for Paper "Understanding Source Code Comments at Large Scale"

Hao He. 2019. Understanding Source Code Comments at Large-Scale. In Proceedings of the 27th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE ’19), August 26–30, 2019, Tallinn, Estonia. ACM, New York, NY, USA, 3 pages. https://doi.org/10.1145/3338906.3342494 

## Replication

### Download and Generate CSV Data

By downloading the latest data from GitHub, the results will differ from those in paper. In order to replicate exactly what is in the paper, you need to skip this step and use data in `result/` folder.

```
# Make sure that your disk have at least 50GB empty space
mkdir temp
python repo_info_download.py [GitHub Username] [GitHub Access Token]
python download2.py
python contributor_info_download.py [JSON File] [GitHub Username] [GitHub Access Token]
python repo_info_analysis.py
```

### Analysis and Visualization

See `visualization.ipynb`. The scripts must be run from the first to the last.