# Generate random initial_prevalence.csv
# 140731 - Initial version (jep)

NMATRIX = 3

#
# !!!
# BE CAREFUL TO CHANGE HScat if health states are changing !!!
# !!!
#

HScat = c("age", "M", "S1", "S2", "I1", "I2", "I3", "PV", "PP")
Agecat = c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "24", "36", "48", "60", "72", "84", "96", "108", "120", "132", "144", "156", "168", "180", "192", "204", "216", "228", "240", "252", "264", "276", "288", "300", "312", "324", "336", "348", "360", "372", "384", "396", "408", "420", "432", "444", "456", "468", "480", "492", "504", "516", "528", "540", "552", "564", "576", "588", "600", "612", "624", "636", "648", "660", "672", "684", "696", "708", "720", "732", "744", "756", "768", "780", "792", "804", "816", "828", "840", "852", "864", "876", "888")

ageDummy = c(0)

for(i in seq(1, NMATRIX, 1)) {
  
  m = data.frame()
  
  for(j in seq(1, length(Agecat), 1)) {
    #n = runif(length(HScat) - 1, 0, 1)
    #n = rnorm(length(HScat) - 1, mean=runif(1, 0, 1), sd=25)
    n = rpois(length(HScat) - 1, lambda=2)
    s = sum(n)
    n = n/s
    n = append(ageDummy, n)
    m = rbind(m, n)
  }
  
  colnames(m) = HScat
  
  m[,1] = Agecat
  
  #write.csv(m, file=paste("initial_prevalence_ru", i, ".csv", sep=""), row.names = FALSE)
  #write.csv(m, file=paste("initial_prevalence_rn", i, ".csv", sep=""), row.names = FALSE)
  write.csv(m, file=paste("initial_prevalence_rp", i, ".csv", sep=""), row.names = FALSE)
}
