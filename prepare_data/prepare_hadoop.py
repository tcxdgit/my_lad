# coding:utf-8
import os
import re

hadoop_dir = ""

# log_format = 'LineId,Date,Time,Level,Process,Component,Content'  # Hadoop log format

# hadoop_file = os.path.join(hadoop_dir, "HDFS.log")
anomaly_label_file = os.path.join(hadoop_dir, "anomaly_label.csv")

normal_dirnames = []
with open(anomaly_label_file, "r", encoding="utf-8") as f_label:
    normal = False
    for line in f_label.readlines():
        line_clean = line.strip()
        if 'Normal:' in line_clean:
            normal = True
        elif normal and line_clean.startswith('+'):
            normal_dirnames.append(re.sub("\+ ", "",line_clean))
        else:
            normal = False


for normal_dirname in normal_dirnames:
    normal_dir = os.path.join(hadoop_dir, normal_dirname)
    # for dirpath, dirnames, filenames in os.walk(normal_dir):
    for normal_files in os.listdir(normal_dir):






#
# with open(hadoop_file, "r", encoding="utf-8") as f_hadoop:
#     for line in f_hadoop.readlines():



