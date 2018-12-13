# Contributing

Contributions are welcome and are greatly appreciated! Every
little bit helps, and credit will always be given.

# Table of Contents
  * [TOC](#table-of-contents)
  * [Types of Contributions](#types-of-contributions)
      - [Report Bugs](#report-bugs)
      - [Fix Bugs](#fix-bugs)
      - [Implement Features](#implement-features)
      - [Improve Documentation](#improve-documentation)
      - [Submit Feedback](#submit-feedback)
  * [Documentation](#documentation)
  * [Development and Testing](#development-and-testing)
      - [Setting up a development environment](#setting-up-a-development-environment)
      - [Running unit tests](#running-unit-tests)
  * [Pull requests guidelines](#pull-request-guidelines)

## Types of Contributions

### Report Bugs

Report bugs through [Github Issues](https://github.com/magic-network/magic-agent/issues).

Please report relevant information and preferably code that exhibits
the problem.

### Fix Bugs

Look through the issues for bugs. Anything is open to whoever wants
to implement it.

### Implement Features

Look through the [Github Issues](https://github.com/magic-network/magic-agent/issues) for features. Any unassigned "enhancement" issue is open to whoever wants to implement it.

### Improve Documentation

Magic could always use better documentation, or even on the web as blog posts or
articles.  Official source for documentation are found on [the documentation repository](https://github.com/magic-network/magic-docs).

### Submit Feedback

The best way to send feedback is to open an issue on [Github Issues](https://github.com/magic-network/magic-agent/issues).

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-based project, and that contributions are welcome :)

## Documentation

The latest API documentation is usually available
[here](https://github.com/magic-network/magic-docs), which contains instructions on how to run the docs
locally.

## Development and Testing

### Set up a development environment

There are two ways to setup a Magic Agent development environment.

1. Using tools and libraries installed directly on your system.

    Install Python (3.5.0+) by using system-level package
    managers like yum, apt-get for Linux, or Homebrew for Mac OS at first. Refer to the [base CI Dockerfile](https://github.com/magic-network/magic-agent/blob/master/Dockerfile) for
    a comprehensive list of required packages   
    Then install python development requirements. It is usually best to work in a virtualenv
        
    ```bash
    virtualenv env
    source env/bin/activate
    pip install -e .[devel]
    ```

    Hint: We enjoy use of [pyenv](https://github.com/pyenv/pyenv) & [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) which allows you to
    specify the python version of your environment.

2. Using a Docker container

    Go to your Magic Agent directory and start a new docker container.
      
    ```
    # Start docker in your Magic directory
    docker run -t -i -v `pwd`:/magic-agent/ -w /magic-agent/ python:3 bash
    pip install -e  
    ``` 
    
    The Magic code is mounted inside of the Docker container, so if you change something using your favorite IDE, you can directly test is in the container.

### Running unit tests

Coming soon...

## Pull Request Guidelines

Before you submit a pull request from your forked repo, check that it
meets these guidelines:

1. Every pull request should have an associated [Github Issue](https://github.com/magic-network/magic-agent/issues).
1. Please squash commits and resolve all conflicts.
1. If the pull request adds functionality, the docs should be updated. 
1. Please read this excellent [article](http://chris.beams.io/posts/git-commit/) on commit messages and adhere to them. It makes the lives of those who come after you a lot easier.

