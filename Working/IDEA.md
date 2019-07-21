# Ideas

## Introduction

Source code comments are one of the most important software artifacts produced by programmers during software development. It forms an essential part of documentation, providing additional information not immediately visible from source code

## Research Questions

RQ1: What are the commenting practices in the wild?

RQ2: What are the impact of different commenting practices on a project's popularity, robustness and sustainability?

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

### Metrics Extracted for Each Project