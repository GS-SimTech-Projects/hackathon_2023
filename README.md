# SimTech PhD Retreat Hackathon

This time around, the goal is to collaboratively develop a tool that automates assigning posters to the individual stands at events like the status seminar.

## Scope

The programs functionality can be divided into 4 parts:
1. extracting the information from the input files and represent them as a graph
2. assign posters to the rooms and individual poster walls.
3. assign posters to one of several time slots
4. visually represent the assignment

Assignments should be done such that posters with similar keywords are grouped physically close together and do not temporally overlap.

Make sure to check out the CONTRIBUTING guidelines.

## Specifications

- the programming language is Python
- internal representation of the data should be a networkx graph

## Scope 1 - extracting the information from the input files and represent them as a graph

### Links
- [Seminaris Floor 2](https://my.matterport.com/show/?m=WZbCFTconCW)
- [Seminaris Fact Sheet PDF Link](https://www.seminaris.de/wp-content/uploads/2022/06/seminaris-hotel-badboll-conference-factsheet-A4.pdf)