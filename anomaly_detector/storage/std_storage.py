# coding:utf-8
""" stdin and stdout Storage. """
from anomaly_detector.storage.storage_attribute import DefaultStorageAttribute
from pandas.io.json import json_normalize
from anomaly_detector.storage.storage_sink import StorageSink
from anomaly_detector.storage.storage_source import StorageSource
from anomaly_detector.storage.storage import DataCleaner
import logging
import json

_LOGGER = logging.getLogger(__name__)


class StdStorageDataSink(StorageSink, DataCleaner):
    """Local storage data sink implementation."""

    NAME = "std.sink"

    def __init__(self, configuration):
        """Initialize local storage backend."""
        self.config = configuration

    def store_results(self, data):
        """Store results."""
        if len(self.config.LS_OUTPUT_PATH) > 0:
            with open(self.config.LS_OUTPUT_PATH, self.config.LS_OUTPUT_RWA_MODE) as fp:
                json.dump(data, fp)
        else:
            for item in data:
                _LOGGER.info("Anomaly: %d, Anmaly score: %f" % (item["anomaly"], item["anomaly_score"]))


class StdStorageDataSource(StorageSource, DataCleaner):
    """Local storage Data source implementation."""

    NAME = "std.source"

    def __init__(self, configuration):
        """Initialize local storage backend."""
        self.config = configuration

    def retrieve(self, storage_attribute: DefaultStorageAttribute):
        """Retrieve data from local storage."""
        data = []
        message_field = input("please input log >>")
        data.append({"message": message_field})
        data_set = json_normalize(data)
        _LOGGER.info("%d logs loaded", len(data_set))
        self._preprocess(data_set)
        return data_set, data
