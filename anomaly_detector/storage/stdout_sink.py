"""Stdout sink."""
import logging
from anomaly_detector.storage.storage_sink import StorageSink


class StdoutSink(StorageSink):
    """Standard output sink to allow us to help debug."""

    def __init__(self, config):
        """Initialize storage."""
        super(StdoutSink, self).__init__(config)
        self.config = config

    def store_results(self, entries):
        """Sink stores results in system.
        We output logs to standard console of what is considered anomaly."""
        logging.info("You can click the following links"
                     " to provide feedback to factstore")
        if self.config.FACT_STORE_URL:
            for entry in entries:
                try:
                    if entry.get('anomaly') == 1:
                        logging.info(
                            "%s?lad_id=%s&is_anomaly=%s&message=%s",
                            self.config.FACT_STORE_URL,
                            entry['predict_id'], "False",
                            entry['e_message'])
                except Exception as error:
                    logging.debug(error)
            logging.info("output logs %s in stdout.sink", len(entries))
        else:
            logging.error("To use stdout.sink "
                          "you must set FACT_STORE_URL config")
