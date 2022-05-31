### Explore results
library(dplyr)
library(foreign)
library(shapefiles)
library(raster)
library(proxy)
library(sp)
library(sf)
library(rgdal)
library(geosphere)
library(Matrix)
setwd("~/Desktop/Research/COVID project/Submission MS/Code")

################################################################################
### Tract

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

demographic_data_state <- demographic_data_state[, c("GIDTR", "County", "County_name", "Tract")]
demographic_data_state$County_name <- gsub("\\s*\\w*$", "", demographic_data_state$County_name)
population_centroids_state <- population_centroids_state %>% left_join(demographic_data_state, by = c("FIPS" = "GIDTR"))
HPI_TRACT = read.csv("../Data/hpitract.csv")
HPI_TRACT$FIPS = paste("0", as.character(HPI_TRACT$geoid), sep="")
population_centroids_state <- population_centroids_state %>% left_join(HPI_TRACT, by = "FIPS")

TRACT_STATE <- na.omit(population_centroids_state)
TRACT_STATE <- TRACT_STATE %>% dplyr::select(c("FIPS", "STATE", "COUNTY", "County_name", "TRACT", "POPULATION", "LATITUDE", "LONGITUDE", "geoid", "HPI", "HPIQuartile"))
write.csv(TRACT_STATE, "../Data/Tract_CA.csv")

##############################################################################
### Import stores

ZIP_HPI <- read.csv("../Data/HPI.csv")

DOLLAR <- read.csv("../Data/Dollar_store_total_USA.csv", stringsAsFactors = FALSE)
DOLLAR = DOLLAR[DOLLAR$State %in% c('CA'), ]
DOLLAR <- DOLLAR %>% dplyr::select(-c("ID"))
DOLLAR <- left_join(DOLLAR, ZIP_HPI, by = c("Zip_Code" = "Zip"))
write.csv(DOLLAR, "../Data/Dollar_stores_CA.csv")

CURRENT <- read.csv("../Data/USA_with_latlong.csv", stringsAsFactors = FALSE)
CURRENT = CURRENT[CURRENT$state %in% c('CA'), ]
CURRENT = subset(CURRENT, select=-c(X,Unnamed..0,Unnamed..0.1,number_in_search,details))
CURRENT$latitude = as.numeric(CURRENT$latitude)
CURRENT$longitude = as.numeric(CURRENT$longitude)
names(CURRENT)[names(CURRENT) == 'latitude'] <- 'Latitude'
names(CURRENT)[names(CURRENT) == 'longitude'] <- 'Longitude'
CURRENT$zip_code = as.character(CURRENT$zip_code)
ZIP_HPI$Zip = as.character(ZIP_HPI$Zip)
CURRENT <- left_join(CURRENT, ZIP_HPI, by = c("zip_code" = "Zip"))
CURRENT <- CURRENT %>% dplyr::select(-c("distance","stock"))
write.csv(CURRENT, "../Data/Current_stores_CA.csv")

