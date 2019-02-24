install.packages("ggplot2")
install.packages("igraph")

library("ggplot2")
library("igraph")

SiteData <- read.csv(file='/home/evan/Documents/Projects/HackIllinois-2019/crawlmap-master/scraper/dataFrame.csv' , header=TRUE, sep=',')

png(width=15000,height=15000,units='px')

network = graph_from_adjacency_matrix(SiteData)

plot(network)

dev.off()
