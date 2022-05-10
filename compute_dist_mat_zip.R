# Compute the distance matrix and demand vector etc. for a given state

# Install and load packages
library(Matrix)

# Packages for parallel computing
library(parallel)
library(MASS)
library(foreach)
library(doParallel)
library(geosphere)

# Set directories
dir = getwd()
setwd(dir)

# Specify state
state = 'CA'
state_ID = "06"

################################################################################

################################# Read file ####################################

################################################################################

### Centers for each zip code
ZIP_STATE <- read.csv("../Data/CaliforniaZip.csv", stringsAsFactors = FALSE)
ZIP_STATE$Lat = as.numeric(ZIP_STATE$Lat)
ZIP_STATE$Lng = as.numeric(ZIP_STATE$Lng)

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
    zip_lat = zip_row$Lat
    zip_lon = zip_row$Lng
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
write.table(dist_matrix, file= paste("../Data/dist_matrix_", state, "_dollar.csv", sep=""), sep=',',
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
    zip_lat = zip_row$Lat
    zip_lon = zip_row$Lng
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

write.table(dist_matrix_current, file = paste("../Data/dist_matrix_", state, "_current.csv", sep=""), sep=',',
            row.names = FALSE, col.names = FALSE)
rm(dist_values_current)
rm(dist_matrix_current)

