# CommentAnalysis
Comment Analysis on Open Source Software Projects

## About this Project
This is a project about analyzing comments in existing open source projects, such as the distribution pattern and content of comments. We plan to work on projects of different programming languages and application domains. After that, we plan to develop an automation tool for identification of poorly commented areas and suggestions about where to add comments and what type of comments to add.

## Project Configuration
### Guidelines
Personally I recommend VS Code with Python extension and Pylint enabled. For coding, the [PEP8 Style Guidelines](https://www.python.org/dev/peps/pep-0008/) should be followed.

No automatically generated data should be uploaded to this repository, except that it is significant result and need to be saved. For temporary data, it should be generated in `temp/` folder. For significant result, it should be manually moved to the `result/` folder.

### Download Projects from GitHub
```
python download.py
```

## Design Considerations
### Retrieving Projects on GitHub
We plan to retrieve projects in the following programming languages.
* C++
* Java
* Python
* Javascript
And the following application domains(GitHub topics)
* Web
* Machine Learning
* Database
* Visual Computing
* Formatting
We manually select 20 repositories from famous open source projects. We have considered using the GitHub API for automatic repository selection based on topics. However, we've found that the GitHub topic system have the following limitations: 
1. Many popular open source repositories have no topic at all.
2. Some generic topics(like `web` and `database`) are not chosen by developers. For example, `mysql` has 1.7x more repositories than `database`, which means that we may miss many potentially representitive projects if we use something like `database` as filter. Therefore, we leave the automatic retrieval of GitHub projects for future work.
