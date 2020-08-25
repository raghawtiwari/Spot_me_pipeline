
# spot_me
### Requirements

 #### Setting Up PySpark
    sudo apt install openjdk-11-jdk 
 Download latest spark hadoop from http://spark.apache.org/downloads.html and exract it 
 
    $ tar -xzf spark-3.0.0-bin-hadoop2.7.tgz
    $ pip3 install pyspark
    $ sudo gedit .bashrc
write folowing and save it 

    export SPARK_HOME=<"path to extracted spark">
    export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.8.1-src.zip:$PYTHONPATH
    export PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$PATH
    export PYSPARK_PYTHON=python3
    export PYSPARK_DRIVER_PYTHON=python3
now open terminal and type

    pyspark 
it will run.


 #### Setting Up Kafka
    Go to official Appache kafka and install kafka in your pc.
   
 ### Setting Up Elasticsearch and reactivesearch
 
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.7.0-linux-x86_64.tar.gz (gettting elasticsearch )
    tar -xzf elasticsearch-7.7.0-linux-x86_64.tar.gz 
    sudo apt install npm 
    npm install @appbseio/reactivesearch 
    npm install -g create-react-app 
    create-react-app   name_of_your_app (It will make a directory named name_of_your_app and install required dependencies to it.)
    
### spark_dependencies

Download following dependencies

    spark-sql-kafka-0-10_2.12-3.0.0-preview.jar
    kafka-clients-2.5.0.jar
    spark-streaming-kafka-0-10-assembly_2.12-3.0.0-preview2.jar
    commons-pool2-2.8.0.jar,elasticsearch-hadoop-7.7.0.jar
    (make sure all dependecies are consistent with the versions of spark and kafka)

### cloning yolov5

    !git clone https://github.com/ultralytics/yolov5 
    !pip install -qr yolov5/requirements.txt  
Check if yolov5 is installed properly by

    cd yolov5
    !python detect.py --source '0' --output './results.avi'
    
    
###### changes to be made in Elasticsearch configuration file 
    • Go to elasticsearch directory (where it was extracted) → config → elasticsearch.yml
    Everything is commented out initially. Things to specify
    • <cluster.name: my_cluster_name>
    • <node.name: node_name>
    • For Master node: <node.master: true>
    • For Data nodes: <node.data: true>
    • <network.host: host_ip_address>
    • <http.port: 9200>
    
## Running
To start kafka server
go inside kafka directory and type 
 
    bin/zookeeper-server-start.sh config/zookeeper.properties
    bin/kafka-server-start.sh config/server.properties
    
runnung elasticsearch and reactivesearch UI

    cd elasticsearch_directory
    bin/elasticsearch 
    cd  name_of_your_app 
    npm start
Now,run producer.py to publish camera feeds then run kafka_spark.py to consume feeds from kafka, run yolov5 and send results to elasticsearch .(Make sure all spark dependencies are on the same directory where producer.py and kafka_spark.py exists. )

### Steps to show images or Videos 
    1. Go to your name_of_your_app/src directory replace App.js code from above App_main.js code similarly for App.css .
    2. Go to name_of_your_app/public directory, copy frame.py and push_to_es.py file here .
    3. run frame.py here with terminal.
    4. run push_to_es.py here with the terminal.
    5. relod the page it must render all images and Videos or images .(in our case it will render only if data pushed to es cluster has the same mapping that i defined in python script.)
