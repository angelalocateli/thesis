# Title: Relationship between air pollutants and respiratory diseases: analysis by spatial data clustering and temporal association rules

The present work has the general objective of applying data mining techniques in order to discover patterns that relate the concentration levels of atmospheric pollutants with rates of occurrence of respiratory diseases, taking into account the geolocation of the patterns and the time intervals in which the patterns happened.

This objective was systematized into specific goals. This repository have all the scripts and instructions to execute.

# Repository:

- Clustering/Clustering_ploter: Explore how the clustering technique can contribute to the discovery of spatial and temporal patterns of pollutants in cities in the State of São Paulo;

- Association_Rules: Investigate, through association rules, considering the groups that present a high concentration of pollutants, co-occurrences between pollutant emission concentration, and meteorological variables in different regions;

- Armada_analysis/Armada_plot (SP, Campinas, Santos): Design and implement an algorithm for extracting temporal association rules for multivariate series in search of frequent patterns, which include temporal intervals and their relationships;

- Armada_functions: Analyze temporal rules that consider higher incidence multi-pollutants in the short-term relationship with the increase in hospitalizations for respiratory diseases, to track the behavior of evolutionary data in the discovery of patterns.

# Runing the scripts: 

The Execution environment was Anaconda (Jupyter Notebook e gerenciador de pacotes pip). Open-source, with environment management system for Python programs, that runs on Windows, macOS, and Linux. For this you can use a docker container.

If you want to run the scripts, clone this repository in your source folder, open a terminal and navigate to the folder where the scripts are located.

Install the necessary libraries to execute the scripts: !pip install <path> . For example: !pip install scikit-learn-extra

All scripts require a .csv file as upload defined in the dataframe (same format).  Also a path for output file (data and graph). It is not recommended to use the same folder for different analyses.
