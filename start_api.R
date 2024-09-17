library(plumber)

api_file <- sprintf("%s/api.R", getwd())

pr(api_file) %>%
  pr_run(port=8077)
