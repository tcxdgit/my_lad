====================
Log Anomaly Detector
====================

Log anomaly detector is an open source project code named "Project Scorpio". LAD is also used for short. It can connect to streaming sources and produce predictions of abnormal log lines. Internally it uses unsupervised machine learning. We incorporate a number of machine learning models to achieve this result. In addition it includes a human in the loop feedback system.

Project background
==================

The original goal for this project was to develop an automated means of notifying users when problems occur with their applications based on the information contained in their application logs. Unfortunately logs are full of messages that contain warnings or even errors that are safe to ignore, so simple “find-keyword” methods are insufficient . In addition, the number of logs are increasing constantly and no human will, or can, monitor them all. In short, our original aim was to employ natural language processing tools for text encoding and machine learning methods for automated anomaly detection, in an effort to construct a tool that could help developers perform root cause analysis more quickly on failing applications by highlighting the logs most likely to provide insight into the problem or to generate an alert if an application starts to produce a high frequency of anomalous logs.

INSTALLING THE PKG
==================

Using pip::

    $ pip install -r requirements

.. note::

   LAD requires python 3.6

USAGE
==================
在config_files\目录下创建配置文件

训练::

    $ python app.py --config-yaml config_files/.env_cmn_log_fmt_config.yaml --single-run True

推理::

    $ python app.py --job-type inference --config-yaml config_files/.env_cmn_log_fmt_config.yaml --single-run True


Documentation
-------------

TODO

