##---------------------------------------------------------------##
##                Load libraries and import data                 ##
##---------------------------------------------------------------##

# Load libraries
library(ggplot2)

# Import data
sc1_steady_before_data <- read.csv("scenario-1/steady-log-pre.csv")
sc1_steady_after_data <- read.csv("scenario-1/steady-log-post.csv")
sc1_overload_data <- read.csv("scenario-1/overload-log.csv")
sc2_steady_before_data <- read.csv("scenario-2/steady-log-pre.csv")
sc2_steady_after_data <- read.csv("scenario-2/steady-log-post.csv")
sc3_steady_before_data <- read.csv("scenario-3/steady-log-pre.csv")
sc3_steady_after_data <- read.csv("scenario-3/steady-log-post.csv")
sc4_steady_before_data <- read.csv("scenario-4/steady-log-pre.csv")
sc4_steady_after_data <- read.csv("scenario-4/steady-log-post.csv")
sc5_steady_before_data <- read.csv("scenario-5/steady-log-pre.csv")
sc5_steady_after_data <- read.csv("scenario-5/steady-log-post.csv")


##---------------------------------------------------------------##
##                   Descriptive Statistics                      ##
##---------------------------------------------------------------##

# Create summary for all datasets
summary(sc1_steady_before_data)
summary(sc1_steady_after_data)
summary(sc1_overload_data)
summary(sc2_steady_before_data)
summary(sc2_steady_after_data)
summary(sc3_steady_before_data)
summary(sc3_steady_after_data)
summary(sc4_steady_before_data)
summary(sc4_steady_after_data)
summary(sc5_steady_before_data)
summary(sc5_steady_after_data)


##---------------------------------------------------------------##
##                       Generate Graphs                         ##
##---------------------------------------------------------------##

# Creates a success scatter plot and saves it to PDF
create_and_save_success_scatter_plot <- function(data, scenario_num, data_label, ylim_lower, ylim_upper) {
  plot_label <- paste("Successful Requests over Time - Scenario", scenario_num, data_label)
  x_label <- "Time (in sec)"
  y_label <- "Number of Succesful Requests"
  
  # Create Plot
  scatter_plot <- ggplot(data=data, aes(x=Target.Time, Successful.Transactions)) +
    geom_point() +
    geom_rug(col="steelblue",alpha=0.1, size=1.5) +
    xlab(x_label) +
    ylab(y_label) +
    labs(title = plot_label) +
    ylim(ylim_lower, ylim_upper)
  
  save_plot(scatter_plot, plot_label)
}

# Creates a fails scatter plot and saves it to PDF
create_and_save_fails_scatter_plot <- function(data, scenario_num, data_label, ylim_lower, ylim_upper) {
  plot_label <- paste("Failed Requests over Time - Scenario", scenario_num, data_label)
  x_label <- "Time (in sec)"
  y_label <- "Number of Failed Requests"
  
  # Create Plot
  scatter_plot <- ggplot(data=data, aes(x=Target.Time, Failed.Transactions)) +
    geom_point() +
    geom_rug(col="steelblue",alpha=0.1, size=1.5) +
    xlab(x_label) +
    ylab(y_label) +
    labs(title = plot_label) +
    ylim(ylim_lower, ylim_upper)
  
  save_plot(scatter_plot, plot_label)
}

# Creates a response time scatter plot and saves it to PDF
create_and_save_response_time_scatter_plot <- function(data, scenario_num, data_label, ylim_lower, ylim_upper) {
  plot_label <- paste("Avg. Response Time over Time - Scenario", scenario_num, data_label)
  x_label <- "Time (in sec)"
  y_label <- "Avg. Response Time (in sec)"
  
  # Create Plot
  scatter_plot <- ggplot(data=data, aes(x=Target.Time, Avg.Response.Time)) +
    geom_point() +
    geom_rug(col="steelblue",alpha=0.1, size=1.5) +
    xlab(x_label) +
    ylab(y_label) +
    labs(title = plot_label) +
    ylim(ylim_lower, ylim_upper)
  
  save_plot(scatter_plot, plot_label)
}

# Saves the given plot as PDF
save_plot <- function(scatter_plot, plot_label) {
  path = paste("./scenario-", scenario_num, "/", sep="")
  dir.create(path, showWarnings = FALSE) # Create directory if it doesn't exist
  ggsave(
    paste(plot_label, ".pdf", sep = ""),
    plot = scatter_plot,
    path = path,
    width = 8,
    height = 6,
    units = "in"
  )
}

# Scenario 1
scenario_num <- 1

# Set y axis the same to allow comparison of graphs
response_ylim_lower <- 0
response_ylim_upper <- 3
success_ylim_lower <- 0
success_ylim_upper <- 20
fails_ylim_lower <- 0
fails_ylim_upper <- 5

# Create graphs for scenario 1
data_label <- "(Steady State Before)"
data <- sc1_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)
data_label <- "(Steady State After)"
data <- sc1_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)
data_label <- "(Overload)"
data <- sc1_overload_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, 1300)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)


# Scenario 2
scenario_num <- 2

# Set y axis the same to allow comparison of graphs
response_ylim_lower <- 0
response_ylim_upper <- 4
success_ylim_lower <- 0
success_ylim_upper <- 20
fails_ylim_lower <- 0
fails_ylim_upper <- 5

# Create graphs for scenario 2
data_label <- "(Steady State Before)"
data <- sc2_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)
data_label <- "(Steady State After)"
data <- sc2_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)

# Scenario 3
scenario_num <- 3

# Set y axis the same to allow comparison of graphs
response_ylim_lower <- 0
response_ylim_upper <- 3
success_ylim_lower <- 0
success_ylim_upper <- 20
fails_ylim_lower <- 0
fails_ylim_upper <- 5

# Create graphs for scenario 3
data_label <- "(Steady State Before)"
data <- sc3_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)
data_label <- "(Steady State After)"
data <- sc3_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)

# Scenario 4
scenario_num <- 4

# Set y axis the same to allow comparison of graphs
response_ylim_lower <- 0
response_ylim_upper <- 3
success_ylim_lower <- 0
success_ylim_upper <- 20
fails_ylim_lower <- 0
fails_ylim_upper <- 20

# Create graphs for scenario 4
data_label <- "(Steady State Before)"
data <- sc4_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)
data_label <- "(Steady State After)"
data <- sc4_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)

# Scenario 5
scenario_num <- 5

# Set y axis the same to allow comparison of graphs
response_ylim_lower <- 0
response_ylim_upper <- 50
success_ylim_lower <- 0
success_ylim_upper <- 80
fails_ylim_lower <- 0
fails_ylim_upper <- 5

# Create graphs for scenario 5
data_label <- "(Steady State Before)"
data <- sc5_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)
data_label <- "(Steady State After)"
data <- sc5_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label, response_ylim_lower, response_ylim_upper)
create_and_save_success_scatter_plot(data, scenario_num, data_label, success_ylim_lower, success_ylim_upper)
create_and_save_fails_scatter_plot(data, scenario_num, data_label, fails_ylim_lower, fails_ylim_upper)
