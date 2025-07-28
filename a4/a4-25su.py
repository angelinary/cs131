from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator

#1
# Initialize spark session
spark = SparkSession.builder.appName("TaxiMLApp").getOrCreate()

# Read the csv file with header
df = spark.read.csv("2019-04.csv", header=True, inferSchema=True)

# Select required columns
df = df.select("passenger_count", "pulocationid", "dolocationid", "total_amount")

# Show first 10 entries
df.show(10)


#2
# Create required DataFrames from the existing data
# Train on a random 80% of the data and test with the remaining 20%
trainDF, testDF = df.randomSplit([0.8, 0.2], seed=42)


#3
# Take the three columns here and treat them as inputs
assembler = VectorAssembler(
    inputCols=["passenger_count", "pulocationid", "dolocationid"],
    outputCol="features"
)

# Treat this column as the output
dt = DecisionTreeRegressor(labelCol="total_amount", featuresCol="features")



#4
# Create a pipeline from the above two steps.
pipeline = Pipeline(stages=[assembler, dt])



#5
# Train the model
model = pipeline.fit(trainDF)


#6
# Test the model and show 10
predictions = model.transform(testDF)
predictions.select("passenger_count", "pulocationid", "dolocationid", "total_amount", "prediction").show(10)


#7
# Show the RMSE
evaluator = RegressionEvaluator(labelCol="total_amount", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE): {rmse}")

