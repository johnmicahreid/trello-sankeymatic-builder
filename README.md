# trello-sankeymatic-builder

A tool to help generate sankey diagrams from trello board activity

Sankey diagrams are great, especially the ones that Sankeymatic helps you build:
http://sankeymatic.com/build/

Trello boards are also great. Why not combine them?

This is a short script to generate sankeymatic input data based on the movement of cards between lists on a trello board. You'll need the following 3 pieces of info:
- Your trello token
- Your trello key
- Your board shortlink

It'll print out info in the following format, which you can just copy paste into sankeymatic:
SOURCE [AMOUNT] DESTINATION

