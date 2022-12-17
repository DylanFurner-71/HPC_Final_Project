import sys
import glob

#sys.path.append('/lib/')
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from sparknlp.base import Finisher, DocumentAssembler
from sparknlp.annotator import (Tokenizer, Normalizer,
                                LemmatizerModel, StopWordsCleaner)
from pyspark.ml import Pipeline
import sparknlp

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: hdfs_wordcount.py <directory>")
        sys.exit(-1)
    # spark = SparkSession.builder \
    #     .appName("Spark NLP")\
    #     .master("local[*]")\
    #     .config("spark.driver.memory","16G")\
    #     .config("spark.driver.maxResultSize", "0") \
    #     .config("spark.kryoserializer.buffer.max", "2000M")\
    #     .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:4.2.5")\
    #     .getOrCreate()
    
    sc = SparkContext(appName="PythonStreamingHDFSWordCount")
    ssc = StreamingContext(sc, 1)
    lines = ssc.textFileStream(sys.argv[1])
    #df1 = sc.read.text(sys.argv[1])
    #df1.show()
    counts = lines.flatMap(lambda line: line.split(" "))\
                .map(lambda x: (x, 1))\
                .reduceByKey(lambda a, b: a + b)
    counts.pprint()
    output = open('output', 'w')
    output.write(counts)
    print(counts)
    print("running")

    ssc.start()
    ssc.awaitTermination()