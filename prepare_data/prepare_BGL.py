# coding:utf-8
import os
import re

BGL_dir = "/root/nlp/tcxia/data/LOGDetection"

# log_format = '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>'

log_file = os.path.join(BGL_dir, "BGL.log")

normal_filename = "bgl_normal.json"
abnormal_filename = "bgl_abnormal.json"

f_normal = open(normal_filename, "w", encoding="utf-8")
f_abnormal = open(abnormal_filename, "w", encoding="utf-8")

data_normal = []
data_abnormal = []

with open(log_file, "r", encoding="utf-8") as f_log:
    for line in f_log.readlines():
        line_tmp = line.strip()
        message_field = " ".join(line.split(" ")[5:])
        message_field = message_field.rstrip("\n")
        if line_tmp.startswith("-"):
            # f_normal.write(line_tmp+"\n")

            data_normal.append({"message": message_field})
        else:
            f_abnormal.write(line_tmp+"\n")

f_normal.close()
f_abnormal.close()
