#!/usr/bin/env python3
# -*- coding: utf-8 -*
import numpy as np
import pandas as pd
import time


def limitToThreshold(threshold, grid):
    grid = grid[(grid.sum_capacity > threshold)]
    return grid


def loadCountry(country, threshold=None):
    filename = "ESSO_1km_" + str(country)
    grid = pd.read_csv(filename + ".csv", sep=";")
    if threshold != None:
        grid = limitToThreshold(threshold, grid)
    return grid


def calculateScenario(sourcecountry, destinationcountry):
    conservation = np.array(sourcecountry.n2000_raster)
    conservation = conservation[~np.isnan(conservation)]
    HFP = np.array(sourcecountry.HFP2009_mean)
    HFP = HFP[(HFP >= -1)]

    cells_matching = destinationcountry[
        (destinationcountry.ws100_mean >= np.percentile(sourcecountry.ws100_mean, 25))&
        (destinationcountry.ws200_mean >= np.percentile(sourcecountry.ws200_mean, 25))&
        (destinationcountry.pop_sum <= np.percentile(sourcecountry.pop_sum, 75))&
        (destinationcountry.elevation_mean <= np.percentile(sourcecountry.elevation_mean, 75))&
        (destinationcountry.LU_3 >= np.percentile(sourcecountry.LU_3, 25))&  # agriculture
        (destinationcountry.LU_4 <= np.percentile(sourcecountry.LU_4, 75))&  # forest
        (destinationcountry.HFP2009_mean >= np.percentile(HFP, 25))&
        (destinationcountry.HFP2009_mean <= np.percentile(HFP, 75))&
        (destinationcountry.n2000_raster <= np.percentile(conservation, 75))
    ]
    return cells_matching


def writePandas(grid, cells_matching, filename):
    result = pd.DataFrame(data={
        "resolution": ["1km"],
        "area_[km2]": [len(cells_matching)],
        "density_Mean_[MW/km2]": [np.mean(sourcecountry.sum_capacity)],
        "capacity_[MW]": [len(cells_matching)*np.mean(sourcecountry.sum_capacity)],
        }
    )
    result.to_csv(filename + time.strftime("_%Y%m%d-%H%M%S") + ".csv", index=False)


if __name__ == "__main__":
    capacitythreshold = 0
    sourcecountry = loadCountry("aut", capacitythreshold)

    destinationcountry = loadCountry("cz")

    cells_matching = calculateScenario(sourcecountry, destinationcountry)
    writePandas(sourcecountry, cells_matching, "Output")