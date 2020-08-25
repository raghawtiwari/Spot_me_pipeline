from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
import sys
import base64
import time
import json
 
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10-assembly_2.12:3.0.0-preview2,org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0, org.apache.kafka:kafka-clients:2.3.0 pyspark-shell'

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.elasticsearch:elasticsearch-hadoop:7.7.0 pyspark-shell'

KAFKA_TOPIC_NAME_CONS = "hello"
KAFKA_OUTPUT_TOPIC_NAME_CONS = "outputtopic"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

c=0

es_write_conf = {
        "es.nodes" : "localhost",
        "es.port" : "9200",
        "es.resource" : 'practice1/docs',
        "es.input.json": "false",
        
    }

if __name__ == "__main__":
    print("Integrating Kafka, Spark And ES...Demo Application Started ...")
    
    
    
    spark = SparkSession\
        .builder\
        .appName("StructuredNetwork")\
        .master("local[*]") \
        .config("spark.jars", "spark-sql-kafka-0-10_2.12-3.0.0-preview.jar,kafka-clients-2.5.0.jar,spark-streaming-kafka-0-10-assembly_2.12-3.0.0-preview2.jar,commons-pool2-2.8.0.jar") \
        .config("spark.executor.extraClassPath", "spark-sql-kafka-0-10_2.12-3.0.0-preview.jar,kafka-clients-2.5.0.jar,spark-streaming-kafka-0-10-assembly_2.12-3.0.0-preview2.jar,commons-pool2-2.8.0.jar,elasticsearch-hadoop-7.7.0.jar") \
        .config("spark.executor.extraLibrary", "spark-sql-kafka-0-10_2.12-3.0.0-preview.jar,kafka-clients-2.5.0.jar,spark-streaming-kafka-0-10-assembly_2.12-3.0.0-preview2.jar,commons-pool2-2.8.0.jar,elasticsearch-hadoop-7.7.0.jar,elasticsearch-spark-20_2.11-7.7.0.jar") \
        .config("spark.driver.extraClassPath", "spark-sql-kafka-0-10_2.12-3.0.0-preview.jar,kafka-clients-2.5.0.jar,spark-streaming-kafka-0-10-assembly_2.12-3.0.0-preview2.jar,commons-pool2-2.8.0.jar,elasticsearch-hadoop-7.7.0.jar") \
        .getOrCreate()

        

    spark.sparkContext.setLogLevel("ERROR")
    vid_detail_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS) \
        .option("subscribe", KAFKA_TOPIC_NAME_CONS) \
        .option("startingOffsets", "latest") \
        .option("enable.auto.commit","true")\
        .load()


    print("Printing Schema of image_data: ")

    print(type(vid_detail_df))

    vid_detail_df.printSchema()
     
    detail_df1 = vid_detail_df.selectExpr("CAST(value AS STRING)")
    timestamp = vid_detail_df.selectExpr("CAST(timestamp AS STRING)")
    #defining the schema for mine data or message i send.
    
    vid_detail_schema = StructType() \
        .add("camera_id", IntegerType()) \
        .add("date", StringType()) \
        .add("time", StringType()) \
        .add("rows", IntegerType()) \
        .add("cols", IntegerType()) \
        .add("data", StringType())

    vid_detail_df2 = detail_df1\
        .select(from_json(col("value"), vid_detail_schema).alias("video_detail"))

    vid_detail_df3 = vid_detail_df2.select("video_detail.data","video_detail.date","video_detail.time","video_detail.camera_id")

    def getrows(df, rownums=None):
        return df.rdd.zipWithIndex().filter(lambda x: x[1] in rownums).map(lambda x: x[0])

    def foreach_batch_function(df, epoch_id):
        
        img = getrows(df, rownums=[0]).collect()
    
        global c
        global es_write_conf 
        
        x="/images/results/img_%s.jpg/img_%s.jpg"%(str(c),str(c))
        es_con ={'data':eval(img[0][0]),'val':x,'date':img[0][1],'time':img[0][2],'camera_id':img[0][3]}
        
        rdd=spark.sparkContext.parallelize([es_con])
        new_rdd=rdd.map(lambda x: ('key',x))
        new_rdd.saveAsNewAPIHadoopFile(path='_',
        outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
        keyClass="org.apache.hadoop.io.NullWritable",
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
        conf=es_write_conf
        )
        
        #Converting string back to .jpg format and storing it locally
        
        file = open("./images/img_%s.jpg"%str(c),'wb')
        file.write(base64.decodestring(eval(img[0][0])))
        file.close()
        os.system("python3 /home/raghaw/yolov5/detect.py --source ./image/public/images/img_%s.jpg --output '/home/raghaw/image/public/images/results/img_%s.jpg'"%(str(c),str(c)))
        c+=1
        
    vid_detail_write_stream = vid_detail_df3.writeStream.foreachBatch(foreach_batch_function).start()

    vid_detail_write_stream.awaitTermination()


    print("PySpark Structured Streaming with Kafka Demo Application Completed....")
