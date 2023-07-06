# Welcome to the SimTech PhD Retreat 2023 Hackathon Contribution Guidelines!

Thank you for participating this years collaborative hackathon.

This guide will give you an introduction to the contribition workflow of this project.

## Getting Started

After you have made a plan and divided tasks in your group, start by cloning this repository.

```
git clone https://github.com/GS-SimTech-Projects/hackathon_2023.git
```

Next you need to install Poetry and create a new Python environment using Poetry itself, conda, or other tools.

You can install the required packages with

```
poetry install
```

in the rootfolder of the project.

Create a new feature branch and start working. Good luck!

## Contributing a new feature

Development is setup with a development branch for every group.
New features should be implemented in indiviual feature branches and merged into the group branch using pull requests upon completion.
It is convenient to designate someone in the group to manage and review pull requests. For each features small unit test should be written bevor starting a pull requests.

Once a group is finished with their tasks, the group branch can be merged into main.

We have set up GitHub actions for running tests linting.
Linting is done with black and isort, so make sure to run them manually or via a pre-commit hook before creating a pull request.
