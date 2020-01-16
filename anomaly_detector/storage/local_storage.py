"""Local Storage."""
import logging
import json
from pandas.io.json import json_normalize
from anomaly_detector.storage.storage_attribute import DefaultStorageAttribute
from anomaly_detector.storage.storage_sink import StorageSink
from anomaly_detector.storage.storage_source import StorageSource
from anomaly_detector.storage.storage import DataCleaner


_LOGGER = logging.getLogger(__name__)


class LocalStorageDataSink(StorageSink, DataCleaner):
    """Local storage data sink implementation."""

    NAME = "local.sink"

    def __init__(self, configuration):
        """Initialize local storage backend."""
        super(LocalStorageDataSink, self).__init__(configuration)
        self.config = configuration

    def store_results(self, data):
        """Store results."""
        if len(self.config.LS_OUTPUT_PATH) > 0:
            with open(
                    self.config.LS_OUTPUT_PATH,
                    self.config.LS_OUTPUT_RWA_MODE) as f_store:
                json.dump(data, f_store)
        else:
            for item in data:
                _LOGGER.info("Anomaly: %d, Anomaly score: %f",
                             item["anomaly"],
                             item["anomaly_score"])


class LocalStorageDataSource(StorageSource, DataCleaner):
    """Local storage Data source implementation."""

    NAME = "local.source"

    def __init__(self, configuration):
        """Initialize local storage backend."""
        super(LocalStorageDataSource, self).__init__(configuration)
        self.config = configuration

    def retrieve(self, storage_attribute: DefaultStorageAttribute):
        """Retrieve data from local storage."""
        data = []
        _LOGGER.info("Reading from %s",
                     self.config.LS_INPUT_PATH)

        with open(self.config.LS_INPUT_PATH, "r") as f_source:
            if self.config.LS_INPUT_PATH.endswith("json"):
                data = json.load(f_source)
            else:
                # Here we are loading in data from common log format
                # Columns [0]= timestamp [1]=severity [2]=msg
                for line in f_source:
                    message_field = " ".join(line.split(" ")[2:])
                    message_field = message_field.rstrip("\n")
                    data.append({"message": message_field})
            if storage_attribute.false_data is not None:
                data.extend(storage_attribute.false_data)
        print("Data format:\n{}".format(data[:5]))
        data_set = json_normalize(data)
        _LOGGER.info("%d logs loaded", len(data_set))
        self._preprocess(data_set)
        return data_set, data
