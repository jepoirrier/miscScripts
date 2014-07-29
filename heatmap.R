# R script to read matrix in CSV and display heatmap
ip = read.csv('heatmapdata.csv', header=TRUE, colClasses = c("factor", "double", "double", "double", "double", "double", "double", "double", "double"))
row.names(ip) = ip$age
ip = ip[,2:length(ip)]
ip = data.matrix(ip)
ip_heatmap = heatmap(ip, Rowv=NA, Colv=NA, col=topo.colors(256), scale="column")
