# Ideas

## Introduction

Source code comments are one of the most important software artifacts produced by programmers during software development. It forms an essential part of documentation, providing additional information not immediately visible from source code. However, comments are also notorious for its scarcity and inconsistency with source code. To address these issues, there are a number of "best practices" in the wild, while their impact on a project remain unclear. Therefore, this research project aims to understand the commenting practices and give practical insights about how to write comments.

## Research Questions

RQ1: What are the commenting practices in the wild?

RQ2: What are the impact of different commenting practices on a project's popularity, robustness and sustainability?

## Methodology

We use projects from JavaScript, Java and Python because they are easy to parse and have clear separation between documentation comments and implementation comments

To answer RQ1, we collect the following metrics for each project and present our results

1. Line of code and Line of comments. Comment density = line of comment / line of code
2. Number of implementation comments and number of documentation comments
3. Percentage of functions with a documentation comment
4. Percentage of files with a header comment
5. Vocabulary used in a comment
6. A list of files and per file metrics like header comment length, documentation comment length, etc

To answer RQ2, we conduct xxx and xxx analysis on the previously collected data

1. We measure a projects' popularity by its number of stars, forks, contributors and used_by, if applicable
2. We measure a projects' robustness by … (Not determined yet)
3. We measure a projects' sustainability by … (Not determined yet)

## How other people think about comments

1. From the Software Engineering Literature
   1. Comment is an important part of artifacts in software, and is part of software documentation
   2. Comment helps in program comprehension and software maintenance
   3. Comment code inconsistencies are very bad. We can discover them using automation tools
2. From Books like "Clean Code" and "Code Complete"
   1. Code is more often read than written
   2. Bad comment is worse than no comment
   3. Comment cannot save bad code. If your code is clear, there is no need for you to write comments
3. From Google Code Style Guides ( Summarized from Python, Java, JavaScript Guides)
   1. It is important that your comment is easily readable, with proper punctuation, spelling and grammar.
   2. You should not write descriptive comments. You should write explanatory comments on tricky part of code. For example
      1. Explain why an exception is caught but not dealt with
      2. Explain side effects of some code
      3. Fall throughs in `switch` statements
   3. It is important to format your documentation comments well enough that others can use your code without looking at your code, but some code entities do not need documentation comments if they are **trivial** and not **externally visible**.
   4. Use `TODO` comments for code that is temporary, a short-term solution, or good-enough but not perfect.
   5. A file header comment is generally helpful but not required (JavaScript Guide)
   6. The best code is self-documenting (C++ Guide)

## Methodology

### Project Filtering

We use a combination of GHTorrent, World of Code and GitHub API. We have collected approcimately 50000 projects. The major programming languages of these projects are either Java, JavaScript, Python, C, C++ or Go.

### Labels Assigned to Each Project

1. Type
   * Software Reuse
      * Library (provide a set of functionalities for use in any code)
      * Framework (provide solution to some specific application like web, need major code modification for integration)
      * Language (e.g. query language, programming language)
   * User Oriented
      * Application (e.g. Android apps, desktop apps, Web apps, etc)
      * Tool (command line or GUI tool for a specific purpose, like compiler)
      * Service (for running on a server)
      * System (e.g. a database system, a distributed data management system or a driver)
      * Plugin (need to be installed on another software, e.g. game mods or IDE plugins)
   * Educational 
      * Examples (examples for using a library, framework or for building a specific type of application, and reference implementation of a specification)
      * Tutorials (a deliberately designed tutorial for a specific topic)
      * Notes (example code or blogs with no specific topic)
      * Books (code in a book related to programming)
   * Unknown
      * We are unable to identify the repository's type based on public information from GitHub
2. Background
   * Industry (must satisfy the following two conditions)
      * The GitHub repository belongs to an account that clearly indicates it is a company
      * The top contributor is employed by the company according to GitHub profile
   * Organization (must satisfy the following three conditions)
      * The GitHub repository belongs to an organization account
      * The organization has an official website
      * The organization account has more than 3 different repositories
   * Unknown
      * Cannot be classified to the above two categories
      * We are not sure whether it is a company sponsored, organized by an open source organization, academic or individual project

### Metrics Extracted for Each Project

1. Stars, forks, authors, commits and number of source files
2. Line of code, line of comments, blank lines
3. Number of documentation comments, number of implementation comments
4. Number of functions and number of functions with documentation comments
5. Number of files with a descriptive file header