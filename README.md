# Assessing land availability for the installation of wind power
This repository contains a basic script which can be used to calculate observation-based estimates of land availability for wind power turbines. 

## How-to
Download the tabular data set from http://dx.doi.org/10.17632/phm6cbdyyd.1 which features site characteristics of raster pixels in Austria, Denmark and Czechia. Information on existing wind power turbines have been mapped with data on wind speeds, land use and nature conservation. For a detailed description of the method, please see the paper Nitsch et al. (2019).

The script allows the user to calculate own scenarios based on the provided data. For each category, specific thresholds can be defined in the `calculateScenario` function which will then limit the area to the sites matching all threshold criteria. 

The `sourcecountry` is the country from which the thresholds should be derived, whereas the `destinationcountry` is the country where the thresholds should be applied to. 

The script is parametrized for a basis specification where the first and the third quartile are used as lower and upper thresholds. You can calculate your own scenarios be changing the filter conditions, respectively. 

## Paper
Nitsch F, Turkovska O, Schmidt J (2019). Observation-based estimates of land availability for wind power: a case study for Czechia. Submitted to Energy, Sustainability and Society.

## Data
Nitsch F, Schmidt J (2019) Site characteristics of current wind power deployment in Austria and Denmark. Mendeley Data, v1 http://dx.doi.org/10.17632/phm6cbdyyd.1 Accessed 1 April 2019.
