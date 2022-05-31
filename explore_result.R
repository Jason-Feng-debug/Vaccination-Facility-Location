library(tidyverse)
library(scales)
library(ggridges)
library(viridis)
library(ggplot2)
library(xtable)
library(dplyr)

setwd("~/Desktop/Research/COVID project/Submission MS/Code")

##############################################################################
### Import
CA_0.7 <- read.csv("../Result/Tract_0.7capacity_N10/CA_Tract_N10.csv")
CA_0.7_new <- read.csv("../Result/Tract_0.7capacity_N10/CA.csv")
CA_0.84 <- read.csv("../Result/Tract_0.84capacity_N10/CA_Tract_N10.csv")
CA_0.84_new <- read.csv("../Result/Tract_0.84capacity_N10/CA.csv")
DOLLAR <- read.csv("../Result/Tract_0.7capacity_N10/DollarStores_Tract_N10.csv")
CURRENT <- read.csv("../Result/Tract_0.7capacity_N10/CurrentStores_Tract_N10.csv")
z_total = read.table("../Result/Tract_0.7capacity_N10/Dist/z_total.csv")
z_total_hpi = read.table("../Result/Tract_0.7capacity_N10/HPI_Dist/z_total.csv")

CURRENT <- read.csv("../Data/Current_stores_CA.csv") 

CURRENT <- read.csv("../Data/CurrentStoresCounty.csv") 
write.csv(CURRENT, "../Data/CurrentStoresCounty.csv")

current <- z_total[1:4035,]
current_hpi <- z_total_hpi[1:4035,]
dollar <- z_total[4036:5051,]
dollar_hpi <- z_total_hpi[4036:5051,]

##############################################################################
### Differences

## Common
sum((current_hpi) == 1 & (current == 1))
CURRENT_COMMON <- CURRENT[current_hpi == 1 & current == 1,]
sum((dollar_hpi) == 1 & (dollar == 1))
DOLLAR_COMMON <- DOLLAR[dollar_hpi == 1 & dollar == 1,]

## Exclusive
DOLLAR_SELECTED_ONLY <- DOLLAR[dollar == 1 & dollar_hpi == 0,]
DOLLAR_HPI_SELECTED_ONLY <- DOLLAR[dollar_hpi == 1 & dollar == 0,]
CURRENT_SELECTED_ONLY <- CURRENT[current == 1 & current_hpi == 0,]
CURRENT_HPI_SELECTED_ONLY <- CURRENT[current_hpi == 1 & current == 0,]

## Quartile
# Current
nrow(CURRENT_COMMON[CURRENT_COMMON$HPIQuartile == 1,])
nrow(CURRENT_COMMON[CURRENT_COMMON$HPIQuartile == 2,])
nrow(CURRENT_COMMON[CURRENT_COMMON$HPIQuartile == 3,])
nrow(CURRENT_COMMON[CURRENT_COMMON$HPIQuartile == 4,])

nrow(CURRENT_SELECTED_ONLY[CURRENT_SELECTED_ONLY$HPIQuartile == 1,])
nrow(CURRENT_HPI_SELECTED_ONLY[CURRENT_HPI_SELECTED_ONLY$HPIQuartile == 1,])

nrow(CURRENT_SELECTED_ONLY[CURRENT_SELECTED_ONLY$HPIQuartile == 2,])
nrow(CURRENT_HPI_SELECTED_ONLY[CURRENT_HPI_SELECTED_ONLY$HPIQuartile == 2,])

nrow(CURRENT_SELECTED_ONLY[CURRENT_SELECTED_ONLY$HPIQuartile == 3,])
nrow(CURRENT_HPI_SELECTED_ONLY[CURRENT_HPI_SELECTED_ONLY$HPIQuartile == 3,])

nrow(CURRENT_SELECTED_ONLY[CURRENT_SELECTED_ONLY$HPIQuartile == 4,])
nrow(CURRENT_HPI_SELECTED_ONLY[CURRENT_HPI_SELECTED_ONLY$HPIQuartile == 4,])

# Dollar
nrow(DOLLAR_COMMON[DOLLAR_COMMON$HPIQuartile == 1,])
nrow(DOLLAR_COMMON[DOLLAR_COMMON$HPIQuartile == 2,])
nrow(DOLLAR_COMMON[DOLLAR_COMMON$HPIQuartile == 3,])
nrow(DOLLAR_COMMON[DOLLAR_COMMON$HPIQuartile == 4,])

nrow(DOLLAR_SELECTED_ONLY[DOLLAR_SELECTED_ONLY$HPIQuartile == 1,])
nrow(DOLLAR_HPI_SELECTED_ONLY[DOLLAR_HPI_SELECTED_ONLY$HPIQuartile == 1,])

nrow(DOLLAR_SELECTED_ONLY[DOLLAR_SELECTED_ONLY$HPIQuartile == 2,])
nrow(DOLLAR_HPI_SELECTED_ONLY[DOLLAR_HPI_SELECTED_ONLY$HPIQuartile == 2,])

nrow(DOLLAR_SELECTED_ONLY[DOLLAR_SELECTED_ONLY$HPIQuartile == 3,])
nrow(DOLLAR_HPI_SELECTED_ONLY[DOLLAR_HPI_SELECTED_ONLY$HPIQuartile == 3,])

nrow(DOLLAR_SELECTED_ONLY[DOLLAR_SELECTED_ONLY$HPIQuartile == 4,])
nrow(DOLLAR_HPI_SELECTED_ONLY[DOLLAR_HPI_SELECTED_ONLY$HPIQuartile == 4,])

##############################################################################
### Explore the differences in location
CA_ZIP <- read.csv("../Data/CaliforniaZipHPI.csv")
CA_ZIP$Zip = as.character(CA_ZIP$Zip)
DOLLAR_SELECTED_ONLY$Zip_Code = as.character(DOLLAR_SELECTED_ONLY$Zip_Code)
DOLLAR_HPI_SELECTED_ONLY$Zip_Code = as.character(DOLLAR_HPI_SELECTED_ONLY$Zip_Code)

DOLLAR_SELECTED_ONLY_INFO <- left_join(DOLLAR_SELECTED_ONLY, CA_ZIP, by = c("Zip_Code" = "Zip"))
DOLLAR_HPI_SELECTED_ONLY_INFO <- left_join(DOLLAR_HPI_SELECTED_ONLY, CA_ZIP, by = c("Zip_Code" = "Zip"))

nrow(DOLLAR_SELECTED_ONLY_INFO[DOLLAR_SELECTED_ONLY_INFO$HPIQuartile == 4,])
nrow(DOLLAR_HPI_SELECTED_ONLY_INFO[DOLLAR_HPI_SELECTED_ONLY_INFO$HPIQuartile == 4,])

##############################################################################
### Map
readRenviron("~/.Renviron")
options(tigris_use_cache = TRUE)
county_shape = get_acs(state = "CA", geography = "county", variables = "B19013_001", geometry = TRUE)
names(county_shape)[names(county_shape) == 'GEOID'] = "FIPS"

county_shape %>%
  st_transform(crs = "+init=epsg:4326") %>%
  leaflet() %>%
  addProviderTiles(provider = "CartoDB.Positron") %>%
  addPolygons(popup = ~ str_extract(NAME, "^([^,]*)"), stroke = FALSE, smoothFactor = 0, fillOpacity = 0.1) %>%
  addCircles(lng=DOLLAR_SELECTED_ONLY$Longitude, lat=DOLLAR_SELECTED_ONLY$Latitude, color = "firebrick", opacity=0.7) %>%
  addRectangles(lng1=DOLLAR_HPI_SELECTED_ONLY$Longitude-0.05, lng2=DOLLAR_HPI_SELECTED_ONLY$Longitude+0.05, 
                lat1=DOLLAR_HPI_SELECTED_ONLY$Latitude-0.05, lat2=DOLLAR_HPI_SELECTED_ONLY$Latitude+0.05, 
                color = "deepskyblue", fillColor = "deepskyblue", weight=1, 
                opacity=0.7, fillOpacity=0.7, popup=~DOLLAR_HPI_SELECTED_ONLY$Address) %>%
  addLegend("bottomleft", colors = c("firebrick", "deepskyblue"), 
            labels = c("Only selected by f_D", "Only selected by f_DH"), 
            title= "Dollar Stores", opacity = 0.9)

##############################################################################
### Distance distribution
CA_HPI4 = CA[CA$HPIQuartile == 4,]
CA_HPI4 = CA_HPI4 %>% filter(Population>0)

CURRENT_HPI = data.frame(DistanceKM = rep(CA$Dist_Current_DistHPI/1000, CA$Population))
BOTH_HPI = data.frame(DistanceKM = rep(CA$Dist_Total_DistHPI/1000, CA$Population))
CURRENT_HPI$Scenario = "Current DistHPI"
BOTH_HPI$Scenario = "Both DistHPI"
ALL = rbind(CURRENT_HPI, BOTH_HPI)
ALL$Scenario = factor(ALL$Scenario, levels=c("Current DistHPI", "Both DistHPI"))

ggplot(ALL, aes(x=ifelse(DistanceKM>5, 5, DistanceKM), fill=Scenario, color=Scenario)) +
  geom_density(alpha=0.2,adjust = 5) +
  scale_fill_manual(name = "Potential Locations", values=c("firebrick", "deepskyblue")) +
  scale_color_manual(name = "Potential Locations", values=c("firebrick", "deepskyblue")) +
  scale_x_continuous("Total Distance to Vaccination Site (km)") +
  labs(y = "Density") + 
  theme_bw() +
  theme(axis.text.x = element_text(size=12), 
        axis.text.y = element_text(size=12),
        strip.text.x = element_text(size = 12),
        strip.text.y = element_text(size = 12),
        plot.title = element_text(hjust=1, size=12))


# Actual
CA_0.7$Population_Current_DistHPI = round(CA_0.7$Population * CA_0.7$Rate_Current_DistHPI)
CA_0.7$Population_Total_DistHPI = round(CA_0.7$Population * CA_0.7$Rate_Total_DistHPI)
CA_0.7_HPI1 = CA_0.7[CA_0.7$HPIQuartile == 1,]
CA_0.7_HPI1 = CA_0.7_HPI1 %>% filter(Population>0)
CURRENT_0.7_HPI = data.frame(DistanceKM = rep(CA_0.7_HPI1$Dist_Current_DistHPI/1000, CA_0.7_HPI1$Population_Current_DistHPI))
BOTH_0.7_HPI = data.frame(DistanceKM = rep(CA_0.7_HPI1$Dist_Total_DistHPI/1000, CA_0.7_HPI1$Population_Total_DistHPI))
CURRENT_0.7_HPI$Scenario = "Current DistHPI(0.7)"
BOTH_0.7_HPI$Scenario = "Both DistHPI(0.7)"
ALL_0.7 = rbind(CURRENT_0.7_HPI, BOTH_0.7_HPI)
rm(CURRENT_0.7_HPI)
rm(BOTH_0.7_HPI)

CA_0.84$Population_Current_DistHPI = round(CA_0.84$Population * CA_0.84$Rate_Current_DistHPI)
CA_0.84$Population_Total_DistHPI = round(CA_0.84$Population * CA_0.84$Rate_Total_DistHPI)
CA_0.84_HPI1 = CA_0.84[CA_0.84$HPIQuartile == 1,]
CA_0.84_HPI1 = CA_0.84_HPI1 %>% filter(Population>0)
CURRENT_0.84_HPI = data.frame(DistanceKM = rep(CA_0.84_HPI1$Dist_Current_DistHPI/1000, CA_0.84_HPI1$Population_Current_DistHPI))
BOTH_0.84_HPI = data.frame(DistanceKM = rep(CA_0.84_HPI1$Dist_Total_DistHPI/1000, CA_0.84_HPI1$Population_Total_DistHPI))
CURRENT_0.84_HPI$Scenario = "Current DistHPI(0.84)"
BOTH_0.84_HPI$Scenario = "Both DistHPI(0.84)"
ALL_0.84 = rbind(CURRENT_0.84_HPI, BOTH_0.84_HPI)
rm(CURRENT_0.84_HPI)
rm(BOTH_0.84_HPI)

ALL = rbind(ALL_0.7, ALL_0.84)
rm(ALL_0.7)
rm(ALL_0.84)

ALL$Scenario = factor(ALL$Scenario, levels=c("Current DistHPI(0.7)", "Both DistHPI(0.7)", "Current DistHPI(0.84)", "Both DistHPI(0.84)"))

ggplot(ALL, aes(x=ifelse(DistanceKM>5, 5, DistanceKM), fill=Scenario, color=Scenario)) +
  geom_density(alpha=0.2,adjust = 5) +
  scale_fill_manual(name = "Potential Locations", values=c("firebrick", "deepskyblue", "darkorange", "darkgreen")) +
  scale_color_manual(name = "Potential Locations", values=c("firebrick", "deepskyblue", "darkorange", "darkgreen")) +
  scale_x_continuous("Actual Distance to Vaccination Site (km) for HPI 1") +
  labs(y = "Density") + 
  theme_bw() +
  theme(axis.text.x = element_text(size=12), 
        axis.text.y = element_text(size=12),
        strip.text.x = element_text(size = 12),
        strip.text.y = element_text(size = 12),
        plot.title = element_text(hjust=1, size=12))

rm(ALL)
##############################################################################

# 0.84
ggplot(data = CA_0.84_HPI1, aes(x = Dist_Current_DistHPI/1000, y = Dist_Total_DistHPI/1000)) + 
  geom_point(aes(size=Population), alpha = 0.5, pch = 19, col = "deepskyblue") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5), 
        axis.title.x = element_text(size=10),
        axis.title.y = element_text(size=10),
        panel.spacing.x = unit(1.5, "lines"),
        legend.text = element_text(size=8),
        legend.title = element_text(size=8, face = 'bold'),
        legend.position = "top") +
  labs(x = "Distance current", y = "Distance after")

# 0.7
ggplot(data = CA_0.7_HPI1, aes(x = Dist_Current_DistHPI/1000, y = Dist_Total_DistHPI/1000)) + 
  geom_point(aes(size=Population), alpha = 0.5, pch = 19, col = "deepskyblue") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5), 
        axis.title.x = element_text(size=10),
        axis.title.y = element_text(size=10),
        panel.spacing.x = unit(1.5, "lines"),
        legend.text = element_text(size=8),
        legend.title = element_text(size=8, face = 'bold'),
        legend.position = "top") +
  labs(x = "Distance current", y = "Distance after")

##############################################################################

Compare = data.frame(Population = CA_0.7$Population,
                     Rate_Current_0.7 = CA_0.7$Rate_Current_DistHPI,
                     Rate_Total_0.7 = CA_0.7$Rate_Total_DistHPI,
                     Rate_Current_0.84 = CA_0.84$Rate_Current_DistHPI,
                     Rate_Total_0.84 = CA_0.84$Rate_Total_DistHPI,
                     Actual_Dist_Current_0.7 = CA_0.7$ActualDist_Current_DistHPI,
                     Actual_Dist_Total_0.7 = CA_0.7$ActualDist_Total_DistHPI,
                     Actual_Dist_Current_0.84 = CA_0.84$ActualDist_Current_DistHPI,
                     Actual_Dist_Total_0.84 = CA_0.84$ActualDist_Total_DistHPI)

Compare_new = data.frame(Population = CA_0.7_new$Population,
                         HPI = CA_0.7_new$HPIQuartile,
                         Rate_Current_0.7 = CA_0.7_new$Rate_Current_DistHPI,
                         Rate_Total_0.7 = CA_0.7_new$Rate_Total_DistHPI,
                         Rate_Current_0.84 = CA_0.84_new$Rate_Current_DistHPI,
                         Rate_Total_0.84 = CA_0.84_new$Rate_Total_DistHPI,
                         Vaccinated_Current_0.7 = CA_0.7_new$Rate_Current_DistHPI * CA_0.7_new$Population,
                         Vaccinated_Total_0.7 = CA_0.7_new$Rate_Total_DistHPI * CA_0.7_new$Population,
                         Vaccinated_Current_0.84 = CA_0.84_new$Rate_Current_DistHPI * CA_0.84_new$Population,
                         Vaccinated_Total_0.84 = CA_0.84_new$Rate_Current_DistHPI * CA_0.84_new$Population,
                         Actual_Dist_Current_0.7 = CA_0.7_new$ActualDist_Current_DistHPI,
                         Actual_Dist_Total_0.7 = CA_0.7_new$ActualDist_Total_DistHPI,
                         Actual_Dist_Current_0.84 = CA_0.84_new$ActualDist_Current_DistHPI,
                         Actual_Dist_Total_0.84 = CA_0.84_new$ActualDist_Total_DistHPI)
options(scipen=999)
Compare_new_HPI1 = Compare_new[Compare_new$HPI == 1,]

nrow(Compare_new_HPI1[Compare_new_HPI1$Actual_Dist_Current_0.7 == 0 & Compare_new_HPI1$Actual_Dist_Total_0.7 != 0,])
nrow(Compare_new_HPI1[Compare_new_HPI1$Actual_Dist_Current_0.7 != 0 & Compare_new_HPI1$Actual_Dist_Total_0.7 == 0,])

##############################################################################

### Keep current stores
CURRENT = read.csv('../Data/Current_stores_CA.csv')
DOLLAR = read.csv('../Data/Dollar_stores_CA.csv')

z_total_20 = read.table("../Result/Tract/20/HPI_Dist/z_total.csv")
z_total_50 = read.table("../Result/Tract/50/HPI_Dist/z_total.csv")
z_total_100 = read.table("../Result/Tract/100/HPI_Dist/z_total.csv")

dollar_20 <- z_total_20[4036:5051,]
dollar_50 <- z_total_50[4036:5051,]
dollar_100 <- z_total_100[4036:5051,]

# Selected dollar stores
DOLLAR_SELECTED_20 <- DOLLAR[dollar_20 == 1,]
DOLLAR_SELECTED_50 <- DOLLAR[dollar_50 == 1,]
DOLLAR_SELECTED_100 <- DOLLAR[dollar_100 == 1,]

# HPI
SELECTED_HPI_20 = c(nrow(DOLLAR_SELECTED_20[DOLLAR_SELECTED_20$HPIQuartile == 1,]), 
                     nrow(DOLLAR_SELECTED_20[DOLLAR_SELECTED_20$HPIQuartile == 2,]), 
                     nrow(DOLLAR_SELECTED_20[DOLLAR_SELECTED_20$HPIQuartile == 3,]),
                     nrow(DOLLAR_SELECTED_20[DOLLAR_SELECTED_20$HPIQuartile == 4,]))

SELECTED_HPI_50 = c(nrow(DOLLAR_SELECTED_50[DOLLAR_SELECTED_50$HPIQuartile == 1,]), 
                     nrow(DOLLAR_SELECTED_50[DOLLAR_SELECTED_50$HPIQuartile == 2,]), 
                     nrow(DOLLAR_SELECTED_50[DOLLAR_SELECTED_50$HPIQuartile == 3,]),
                     nrow(DOLLAR_SELECTED_50[DOLLAR_SELECTED_50$HPIQuartile == 4,]))

SELECTED_HPI_100 = c(nrow(DOLLAR_SELECTED_100[DOLLAR_SELECTED_100$HPIQuartile == 1,]), 
                     nrow(DOLLAR_SELECTED_100[DOLLAR_SELECTED_100$HPIQuartile == 2,]), 
                     nrow(DOLLAR_SELECTED_100[DOLLAR_SELECTED_100$HPIQuartile == 3,]),
                     nrow(DOLLAR_SELECTED_100[DOLLAR_SELECTED_100$HPIQuartile == 4,]))

# Selected stores at county level
COUNTY_DOLLAR_20 <- DOLLAR_SELECTED_20 %>% group_by(County) %>% 
  summarize(Num_dollar_selected = n(),
            Num_dollar_selected_HPI1 = sum(HPIQuartile==1),
            Num_dollar_selected_HPI2 = sum(HPIQuartile==2),
            Num_dollar_selected_HPI3 = sum(HPIQuartile==3),
            Num_dollar_selected_HPI4 = sum(HPIQuartile==4))

COUNTY_DOLLAR_50 <- DOLLAR_SELECTED_50 %>% group_by(County) %>% 
  summarize(Num_dollar_selected = n(),
            Num_dollar_selected_HPI1 = sum(HPIQuartile==1),
            Num_dollar_selected_HPI2 = sum(HPIQuartile==2),
            Num_dollar_selected_HPI3 = sum(HPIQuartile==3),
            Num_dollar_selected_HPI4 = sum(HPIQuartile==4))

COUNTY_DOLLAR_100 <- DOLLAR_SELECTED_100 %>% group_by(County) %>% 
  summarize(Num_dollar_selected = n(),
            Num_dollar_selected_HPI1 = sum(HPIQuartile==1),
            Num_dollar_selected_HPI2 = sum(HPIQuartile==2),
            Num_dollar_selected_HPI3 = sum(HPIQuartile==3),
            Num_dollar_selected_HPI4 = sum(HPIQuartile==4))


xtable(COUNTY_DOLLAR_20)
xtable(COUNTY_DOLLAR_50)
xtable(COUNTY_DOLLAR_100)

###############################################################################
# Walkable vs. deserts
CA_desert <- read.csv("../Result/Tract_0.7capacity_N10/CA_desert.csv")

CA_desert$Walkable_Current_HPI = round(CA_desert$Walkable_Current_HPI, 2)
CA_desert$Walkable_Total_HPI = round(CA_desert$Walkable_Total_HPI, 2)
CA_desert$Desert_Current_HPI = round(CA_desert$Desert_Current_HPI, 2)
CA_desert$Desert_Total_HPI = round(CA_desert$Desert_Total_HPI, 2)
CA_desert$Desert_Total_HPI_Population = round(CA_desert$Population * CA_desert$Desert_Total_HPI)

# Deserts
CA_desert_summary = CA_desert %>% filter(Desert_Total_HPI > 0) %>% group_by(County) %>% 
  select(FIPS, Population, HPIQuartile, Desert_Total_HPI, Desert_Total_HPI_Population)
CA_desert_summary <- CA_desert_summary[order(-CA_desert_summary$Desert_Total_HPI_Population),]
CA_desert_summary$FIPS <- as.character(CA_desert_summary$FIPS)

print(xtable(CA_desert_summary), include.rownames=FALSE)
