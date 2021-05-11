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

##---------------------------------------------------------------##
##                   Descriptive Statistics                      ##
##---------------------------------------------------------------##


summary(sc1_steady_before_data)



##---------------------------------------------------------------##
##                       Generate Graphs                         ##
##---------------------------------------------------------------##

# Creates a Scatterplot with the given values and labels and saves it
create_scatter_plot <- function(x, y, x_label, y_label, plot_label) {
  plot(x, y,
       #     xlim=c(0,250) , ylim=c(0,250), 
       pch=18, 
       cex=2, 
       col="#69b3a2",
       xlab=x_label, ylab=y_label,
       main=plot_label
  )
  dev.off()
}

# Creates the file path and file for the given labels
create_path_and_file <- function(plot_label, scenario_num) {
  path = paste("./scenario-", scenario_num, "/", sep="")
  dir.create(path, showWarnings = FALSE) # Create directory if it doesn't exist
  pdf(file = file.path(path, paste(plot_label, ".pdf", sep = "")),   # The directory you want to save the file in
      width = 8, # The width of the plot in inches
      height = 6)
}

# Creates a scatter plot and saves it to PDF
create_and_save_scatter_plot <- function(x_data, y_data, plot_label, x_label, y_label, scenario_num) {
  create_path_and_file(plot_label, scenario_num)
  create_scatter_plot(x_data,
                      y_data,
                      x_label,
                      y_label,
                      plot_label)
}

# Creates a success scatter plot and saves it to PDF
create_and_save_success_scatter_plot <- function(data, scenario_num, data_label) {
  plot_label <- paste("Successful Requests over Time - Scenario", scenario_num, data_label)
  x_label <- "Time (in sec)"
  y_label <- "Succesful Requests"
  x_data <- data$Target.Time
  y_data <- data$Successful.Transactions
  create_and_save_scatter_plot(x_data, y_data, plot_label, x_label, y_label, scenario_num)
}

# Creates a response time scatter plot and saves it to PDF
create_and_save_response_time_scatter_plot <- function(data, scenario_num, data_label) {
  plot_label <- paste("Avg. Response Time over Time - Scenario", scenario_num, data_label)
  x_label <- "Time (in sec)"
  y_label <- "Avg. Response Time (in sec)"
  x_data <- data$Target.Time
  y_data <- data$Avg.Response.Time
  create_and_save_scatter_plot(x_data, y_data, plot_label, x_label, y_label, scenario_num)
}


# ---


# Scenario 1
scenario_num <- 1
data_label <- "(Steady State Before)"
data <- sc1_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)
data_label <- "(Steady State After)"
data <- sc1_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)
data_label <- "(Overload)"
data <- sc1_overload_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)

# Scenario 2
scenario_num <- 2
data_label <- "(Steady State Before)"
data <- sc2_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)
data_label <- "(Steady State After)"
data <- sc2_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)

# Scenario 3
scenario_num <- 3
data_label <- "(Steady State Before)"
data <- sc3_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)
data_label <- "(Steady State After)"
data <- sc3_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)

# Scenario 4
scenario_num <- 4
data_label <- "(Steady State Before)"
data <- sc4_steady_before_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)
data_label <- "(Steady State After)"
data <- sc4_steady_after_data
create_and_save_response_time_scatter_plot(data, scenario_num, data_label)
create_and_save_success_scatter_plot(data, scenario_num, data_label)




