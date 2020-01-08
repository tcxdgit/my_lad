# coding:utf-8
import os
import pandas as pd

hdfs_dir = ""

# log_format = '<Date> <Time> <Pid> <Level> <Component>: <Content>'  # HDFS log format

hdfs_file = os.path.join(hdfs_dir, "HDFS.log")
anomaly_label_file = os.path.join(hdfs_dir, "anomaly_label.csv")

# with open(anomaly_label_file, "r", encoding="utf-8") as f_label:
anomaly_label = pd.read_csv(anomaly_label_file)

with open(hdfs_file, "r", encoding="utf-8") as f_hdfs:
    for line in f_hdfs.readlines():
