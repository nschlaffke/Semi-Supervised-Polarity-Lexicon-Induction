# Convert files to csv

files <- list.files(path="./LMDict", pattern="*.rda", full.names=TRUE, recursive=FALSE)
lapply(files, function(x) {
  filename = load(file = x)
  write.csv(get(filename), file = paste("./LMDictCsv/", filename, ".csv", sep = ""))
})
