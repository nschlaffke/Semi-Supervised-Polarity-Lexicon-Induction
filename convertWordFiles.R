# Convert file to csv

load(file = "./LMDict/LMDuncertainty.rda")
write.csv(LMDpositive, file = "./LMDictCsv/LMDuncertainty.csv")