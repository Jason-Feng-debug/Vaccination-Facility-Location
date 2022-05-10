# Compute distance matrix at tract level, merge with hpi tract

setwd("~/Desktop/Research/COVID_project/Submission MS/Code")
library(foreign)
library(shapefiles)
library(raster)
library(proxy)
library(sp)
library(sf)
library(rgdal)
library(geosphere)
library(Matrix)
library(usmap)
library(dplyr)

# Packages for parallel computing
library(parallel)
library(MASS)
library(foreach)
library(doParallel)
library(geosphere)

################################################################################

state = "CA"
summary_file <- read.csv("../../Data/output.csv", stringsAsFactors = FALSE)
state_id = summary_file[summary_file["state"] == state, ]$i
if (state_id < 10){
  state_id = paste("0", as.character(state_id), sep="")
} else{
  state_id = as.character(state_id)
}

population_centroids <-st_read("../../Data/Census_tract/popctr_tracts2010/popctr_tracts2010.shp")
population_centroids <- as.data.frame(population_centroids)
population_centroids_state = population_centroids[population_centroids["STATE"] == as.character(state_id), ]

demographic_data <- read.csv("../../Data/Census_tract/demographic/pdb2020trv2_us.csv", 
                             stringsAsFactors = FALSE, colClasses = c(Tract = "character", GIDTR = "character"))
demographic_data_state = demographic_data[demographic_data['State'] == as.numeric(state_id), ] 

duplicated_centroid = length(population_centroids_state$FIPS[duplicated(population_centroids_state$FIPS)])
duplicated_demographic = length(demographic_data_state$GIDTR[duplicated(demographic_data_state$GIDTR)])
if(duplicated_demographic > 0){
  demographic_data_state <- aggregate(x=demographic_data_state, by=list(demographic_data_state$GIDTR), function(x) { max(x, na.rm=TRUE) })
}

diff1 <- subset(demographic_data_state$GIDTR, !(demographic_data_state$GIDTR %in% population_centroids_state$FIPS))
diff2 <- subset(population_centroids_state$FIPS, !(population_centroids_state$FIPS %in% demographic_data_state$GIDTR))
if (length(diff1) != 0 || length(diff2) != 0){
  common <- merge(demographic_data_state, population_centroids_state, by.x = "GIDTR", by.y = "FIPS")
  population_centroids_state <- subset(population_centroids_state, population_centroids_state$FIPS %in% common$GIDTR)
  demographic_data_state <- subset(demographic_data_state, demographic_data_state$GIDTR %in% common$GIDTR)
}

rm(demographic_data)
rm(population_centroids)
rm(common)
rm(summary_file)
################################################################################

HPI_TRACT = read.csv("../Data/hpitract.csv")
HPI_TRACT$FIPS = paste("0", as.character(HPI_TRACT$geoid), sep="")
population_centroids_state <- population_centroids_state %>% left_join(HPI_TRACT, by = "FIPS")

# use ZIP for name so that I don't have to change the code...
ZIP_STATE <- na.omit(population_centroids_state)

# Export population and quartile vector
write.table(ZIP_STATE$HPIQuartile, file= paste("../Data/quartile_tract.csv", sep=""), sep=',',
            row.names = FALSE, col.names = FALSE)

write.table(ZIP_STATE$POPULATION, file= paste("../Data/population_tract.csv", sep=""), sep=',',
            row.names = FALSE, col.names = FALSE)

################################################################################

### Locations of current vaccination sites
CURRENT <- read.csv("../Data/USA_with_latlong.csv", stringsAsFactors = FALSE)

### Locations of dollar stores
DOLLAR <- read.csv("../Data/Dollar_store_total_USA.csv", stringsAsFactors = FALSE)

### Extract state level data
CURRENT_STATE = CURRENT[CURRENT$state %in% c(state), ]
CURRENT_STATE$latitude = as.numeric(CURRENT_STATE$latitude)
CURRENT_STATE$longitude = as.numeric(CURRENT_STATE$longitude)
DOLLAR_STATE = DOLLAR[DOLLAR$State %in% c(state), ]

### Clean up space
rm(CURRENT)
rm(DOLLAR)

################################################################################

### Set the number of cores for parallel computing
numCores <- detectCores()
registerDoParallel(numCores - 1)

# Index the dataframe
ZIP_STATE$ID = seq.int(nrow(ZIP_STATE))
DOLLAR_STATE$ID = seq.int(nrow(DOLLAR_STATE))
CURRENT_STATE$ID = seq.int(nrow(CURRENT_STATE))

# ZIP_STATE = ZIP_STATE[1:5,]
# DOLLAR_STATE = DOLLAR_STATE[1:5,]
# CURRENT_STATE = CURRENT_STATE[1:5,]

# DISTANCE MATRIX (DOLLAR STORE)
dist_values = foreach(store_id = 1:nrow(DOLLAR_STATE)) %dopar% {
  store_row = DOLLAR_STATE[DOLLAR_STATE["ID"] == store_id, ]
  store_lat = store_row$Latitude
  store_lon = store_row$Longitude
  
  foreach(zip_id = 1:nrow(ZIP_STATE), .combine=c) %dopar%{
    zip_row = ZIP_STATE[ZIP_STATE["ID"] == zip_id,]
    zip_lat = zip_row$LATITUDE
    zip_lon = zip_row$LONGITUDE
    dist = round(distm(c(store_lon, store_lat), c(zip_lon, zip_lat), fun = distHaversine))
  }
}

dist_matrix <- matrix(0, nrow = nrow(DOLLAR_STATE), ncol = nrow(ZIP_STATE))
for(store_id in 1:nrow(DOLLAR_STATE)){
  for(j in 1:nrow(ZIP_STATE)){
    zip_id = j
    dist_matrix[store_id, zip_id] <- dist_values[[store_id]][j]
  }
}

# Convert into matrix form and rename the rows/columns by its unique store/tract ID
dist_matrix = as.matrix(dist_matrix)
# colnames(dist_matrix) = ZIP_STATE$Zip
# rownames(dist_matrix) = DOLLAR_STATE$Store.No.

# save as csv file
write.table(dist_matrix, file= paste("../Data/dist_matrix_", state, "_dollar_tract.csv", sep=""), sep=',',
            row.names = FALSE, col.names = FALSE)
rm(dist_values)
rm(dist_matrix)

################################################################################

# DISTANCE MATRIX (EXISTING STORE)
dist_values_current = foreach(store_id = 1:nrow(CURRENT_STATE)) %dopar% {
  store_row = CURRENT_STATE[CURRENT_STATE["ID"] == store_id, ]
  store_lat = store_row$latitude
  store_lon = store_row$longitude
  foreach(zip_id = 1:nrow(ZIP_STATE), .combine=c) %dopar%{
    zip_row = ZIP_STATE[ZIP_STATE["ID"] == zip_id,]
    zip_lat = zip_row$LATITUDE
    zip_lon = zip_row$LONGITUDE
    dist = round(distm(c(store_lon, store_lat), c(zip_lon, zip_lat), fun = distHaversine))
  }
}

dist_matrix_current <- matrix(0, nrow = nrow(CURRENT_STATE), ncol = nrow(ZIP_STATE))
for(store_id in 1:nrow(CURRENT_STATE)){
  for(j in 1:nrow(ZIP_STATE)){
    zip_id = j
    dist_matrix_current[store_id, zip_id] <- dist_values_current[[store_id]][j]
  }
}

# Convert into matrix form and rename the rows/columns by its unique store/tract ID
dist_matrix_current = as.matrix(dist_matrix_current)
# colnames(dist_matrix_current) = ZIP_STATE$Zip
# rownames(dist_matrix_current) = CURRENT_STATE$ID

write.table(dist_matrix_current, file = paste("../Data/dist_matrix_", state, "_current_tract.csv", sep=""), sep=',',
            row.names = FALSE, col.names = FALSE)
rm(dist_values_current)
rm(dist_matrix_current)