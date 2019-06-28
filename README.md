# Comment Analysis

Source Code and Data for Paper "Understanding Source Code Comments at Large Scale"

Hao He. 2019. Understanding Source Code Comments at Large-Scale. In Proceedings of the 27th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE ’19), August 26–30, 2019, Tallinn, Estonia. ACM, New York, NY, USA, 3 pages. https://doi.org/10.1145/3338906.3342494 

## Replication

### Download and Generate CSV Data

Make sure that your disk have at least 50GB empty space. 

```
mkdir temp
python repo_info_download.py
python download2.py
python repo_info_analysis.py
```

### Analysis and Visualization

See `visualization.ipynb`.