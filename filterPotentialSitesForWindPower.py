#!/usr/bin/env python3
# -*- coding: utf-8 -*
import numpy as np
import pandas as pd


def loadCountry(country, threshold):
    filename = "ESSO_1km_"+str(country)
    grid = pd.read_csv(filename+".csv",sep=',')
    grid = limitToCountry(country,grid)
    if threshold != "NaN":
        grid = limitToThreshold(threshold, grid)
    return grid


def limitToCountry(country, grid):
    if country == "aut":
        grid = grid[(grid.aut==1.0)]
    elif country == "dk":
        grid = grid[(grid.dk==1.0)]
    elif country == "cz":
        grid = grid[(grid.cz==1.0)]
    elif country == "mix":
        grid = grid[(grid.mix == 1.0)]
    return grid


def limitToThreshold(threshold, grid):
    grid = grid[(grid.sum_capacity > threshold)]
    return grid


def calculateScenario(sourcecountry,destinationcountry):
    conservation = np.array(sourcecountry.n2000_raster)
    conservation = conservation[~np.isnan(conservation)]
    HFP = np.array(sourcecountry.HFP2009_mean)
    HFP = HFP[(HFP >= -1)]

    cells_matching=destinationcountry[(destinationcountry.ws100_mean>=np.percentile(sourcecountry.ws100_mean,25))&
                                   (destinationcountry.ws200_mean>=np.percentile(sourcecountry.ws200_mean, 25))&
                                   (destinationcountry.pop_sum<=np.percentile(sourcecountry.pop_sum,75))&
                                   (destinationcountry.elevation_mean<=np.percentile(sourcecountry.elevation_mean,75))&
                                   (destinationcountry.LU_3>=np.percentile(sourcecountry.LU_3,25))& #agriculture
                                   (destinationcountry.LU_4<=np.percentile(sourcecountry.LU_4,75))& #forest
                                   (destinationcountry.HFP2009_mean>=np.percentile(HFP,25))&
                                   (destinationcountry.HFP2009_mean<=np.percentile(HFP,75))&
                                   (destinationcountry.n2000_raster <= np.percentile(conservation, 75))
                                   ]
    return cells_matching


def writeResultsToCsv(grid,cells_matching,filename):
    with open(filename+".csv", "w") as of:
        of.write("resolution;"
                 "area_inKM2;"
                 "densityMean_inMWKM-2;"
                 "capacity_inMW\n")
        of.write("{:};{:};{:};{:}\n".format(
            "1km",
            len(cells_matching),
            np.mean(grid.sum_capacity),
            len(cells_matching)*np.mean(grid.sum_capacity))
        )


if __name__ == "__main__":
    capacitythreshold = 0.0
    sourcecountry = loadCountry("aut", capacitythreshold)

    capacitythreshold = "NaN"
    destinationcountry = loadCountry("cz", capacitythreshold)

    cells_matching = calculateScenario(sourcecountry, destinationcountry)
    writeResultsToCsv(sourcecountry, cells_matching, "output")