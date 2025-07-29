from pyspark.sql import SparkSession
from pyspark.sql.functions import mean
import matplotlib.pyplot as plt
import pandas
# All imports that we need to make the logic work

def main(): #Declared main, so we wouldn't have to move the remaining two methods to the top. Style choice. 

    # Create Spark session. Use builder pattern to create an entry point for working with spark.
    spark = SparkSession.builder.appName("GroupByAge").getOrCreate()

    # Load CSV file into a DataFrame. First argument is the file name, then we identify that we have a header, and then we ask spark to infer the type of data.
    df = spark.read.csv("Students_Social_Media_Addiction.csv", header=True, inferSchema=True)

    # Group by Age and count participants. Aggregate means to clump unique ages. We find averages for the 2 columns, and deposit them into corresponding new columns
    grouped_female = df.filter("Gender = 'Female'").groupBy("Age").agg(mean("Avg_Daily_Usage_Hours").alias("Avg_Daily_Usage_Hours"), mean("Mental_Health_Score").alias("Mental_Health_Score")).sort("Age")
    # Call the methods, give them some arguments.
    plot_mental_health_and_sm_hours(grouped_female, "Female", "female_plot.png") 
    scatter_plot(grouped_female, "Female", "female_scatter_agg.png")

    # Now do the same for males.
    grouped_male = df.filter("Gender = 'Male'").groupBy("Age").agg(mean("Avg_Daily_Usage_Hours").alias("Avg_Daily_Usage_Hours"), mean("Mental_Health_Score").alias("Mental_Health_Score")).sort("Age")
    plot_mental_health_and_sm_hours(grouped_male, "Male", "male_plot.png")
    scatter_plot(grouped_male, "Male", "male_scatter_agg.png")

    # Plot all females to see if there are any significant outliers. It would be possible to do this first, and then do the above calc from this data.
    df_female = df.filter("Gender = 'Female'").sort("Age")
    scatter_plot(df_female, "Female", "female_scatter_all.png")
    
    # Do the same for males
    df_male = df.filter("Gender = 'Male'").sort("Age")
    scatter_plot(df_male, "Male", "male_scatter_all.png")

    # Stop the Spark session
    spark.stop()

def plot_mental_health_and_sm_hours(df, gender, filename ):
    pdf = df.toPandas()   # pdf = pandas data frame, so we can use it for matplotlib
    fig, ax1=plt.subplots() # creates a figure with multiple axes
    
    # Plot the usage hours on the first axis
    ax1.plot(pdf["Age"], pdf["Avg_Daily_Usage_Hours"], label="Hours", color="tab:red") # "plot" draws lines, whereas "scatter" draws dots.
    ax1.set_xlabel("Age")
    ax1.set_ylabel("Hours" , color="tab:red")
    ax1.tick_params(axis="y") # tick_params sets the ticks on the y axis
    
    ax2=ax1.twinx() #twinx creates a second axis that shares the x axis.
    ax2.plot(pdf["Age"], pdf["Mental_Health_Score"], label="Mental_Health", color="tab:blue")
    ax2.set_ylabel("Mental health", color="tab:blue")

    plt.title(f"Mean Daily Usage Hours by Age ({gender})")  #template, gender is an argument passed in, and format turns it into a string
    fig.tight_layout() #tight_layout is supposed to better position the labels of axes
    plt.savefig(filename)  # saves our images
    plt.close() #cleans up the plot, since it is not auto-cleaned


def scatter_plot(df, gender, filename ):
    pdf = df.toPandas()
    fig = plt.figure() #creates a new figure, since we closed the previous one above
    
    plt.scatter(pdf["Age"], pdf["Avg_Daily_Usage_Hours"])  # "plot" draws lines, whereas "scatter" draws dots.
    plt.xlabel("Age")
    plt.ylabel("Mean Daily Usage Hours")
    plt.title(f"Mean Daily Usage Hours by Age ({gender})")  #template, gender is an argument passed in, and format turns it into a string
    
    fig.tight_layout()
    plt.savefig(filename)
    plt.close()

main()
