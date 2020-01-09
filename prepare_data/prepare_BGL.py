# coding:utf-8
import os
import json
import logging
import random

_LOGGER = logging.getLogger(__name__)

BGL_dir = "/root/nlp/tcxia/data/LOGDetection"

# log_format = '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>'

log_file = os.path.join(BGL_dir, "BGL.log")

normal_filename = "bgl_normal.json"
abnormal_filename = "bgl_abnormal.json"

chlr = logging.StreamHandler()  # 输出到控制台的handler
_LOGGER.addHandler(chlr)
# HOME = os.getcwd()
f_normal = open(os.path.join("../validation_data", normal_filename), "w", encoding="utf-8")
f_abnormal = open(os.path.join("../validation_data", abnormal_filename), "w", encoding="utf-8")

data_normal = []
data_abnormal = []

with open(log_file, "r", encoding="utf-8") as f_log:

    _LOGGER.info("Reading BGL data......")

    for line in f_log.readlines():
        line_tmp = line.strip()
        message_field = " ".join(line.split(" ")[5:])
        message_field = message_field.rstrip("\n")
        if line_tmp.startswith("-"):
            # f_normal.write(line_tmp+"\n")

            data_normal.append({"message": message_field})
        else:
            # f_abnormal.write(line_tmp+"\n")
            data_abnormal.append({"message": message_field})

    _LOGGER.info("%d normal logs saved", len(data_normal))
    _LOGGER.info("%d abnormal logs saved", len(data_abnormal))

json.dump(data_normal, f_normal)
json.dump(data_abnormal, f_abnormal)

f_normal.close()
f_abnormal.close()


train_filename = "bgl_train.json"
with open(os.path.join("../validation_data", train_filename), "w", encoding="utf-8") as f_train:
    num = 0.05 * len(data_normal)
    num = int(num)
    _LOGGER.info("%d normal logs picked", num)
    noise = random.sample(data_abnormal, num)
    data_train = data_normal + noise
    random.shuffle(data_train)
    json.dump(data_train, f_train)



