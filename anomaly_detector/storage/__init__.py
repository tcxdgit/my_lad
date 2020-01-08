"""Storage package for utilizing source and sinks for ETL pipeline."""
from anomaly_detector.storage.local_storage import LocalStorageDataSource, LocalStorageDataSink
from anomaly_detector.storage.local_directory_storage import LocalDirStorage
from anomaly_detector.storage.storage_attribute import DefaultStorageAttribute
# from anomaly_detector.storage.kafka_storage import KafkaSink
from anomaly_detector.storage.storage_catalog import StorageCatalog

__all__ = ['DefaultStorageAttribute', 'LocalDirStorage', 'LocalStorageDataSink',
           'LocalStorageDataSource', 'StorageCatalog']
