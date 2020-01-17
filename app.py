"""restful api implement based on flask"""
import re
import traceback
import json
from flask import Flask, request
from pandas.io.json import json_normalize
from anomaly_detector.config import Configuration
from anomaly_detector.adapters import SomStorageAdapter, SomModelAdapter

CONFIGURATION_PREFIX = "LAD"
CONFIG_YAML = ('/home/my_lad/config_files/'
               '.env_cmn_log_fmt_config.yaml')

CONFIG = Configuration(prefix=CONFIGURATION_PREFIX, config_yaml=CONFIG_YAML)
STORAGE_ADAPTER = SomStorageAdapter(CONFIG)
MODEL_ADAPTER = SomModelAdapter(STORAGE_ADAPTER)
MODEL_ADAPTER.load_w2v_model()
MODEL_ADAPTER.load_som_model()
MEAN, THRESHOLD = MODEL_ADAPTER.set_threshold()


def clean_message(line):
    """Remove all none alphabetical characters from message strings."""
    return "".join(
        re.findall("[a-zA-Z]+", line)
    )


def preprocess(_data):
    """Provide pre-processing for the _data
     before running it through W2V and SOM."""

    def to_str(x_lists):
        """Convert all non-str lists to string lists for Word2Vec."""
        ret = (" ".join([str(y) for y in x_lists])
               if isinstance(x_lists, list)
               else str(x_lists))
        return ret

    for col in _data.columns:
        if col == "message":
            _data[col] = _data[col].apply(clean_message)
        # Leaving only a-z in there as numbers add to anomalousness quite a bit
        else:
            _data[col] = _data[col].apply(to_str)

    _data = _data.fillna("EMPTY")
    return _data


APP = Flask(__name__)


@APP.route("/log/anomalydetector",
           methods=["POST", "GET"])
def r_forecast():
    """RESTFUL API implement"""
    res = None
    if request.method == "GET":
        res = json.dumps({"message": "success", "data": "Hello World!"})
        # return res
    if request.method == "POST":

        try:
            request_data: dict = json.loads(request.data)
            _df = request_data.get("data", None)
            data = []
            if _df is None or len(_df) == 0:
                res = json.dumps({"message": "error: No log data"})
                return res
                # return json.dumps({"message": "error: No log data"})
            for message_field in _df:
                data.append({"message": message_field})
            data_set = json_normalize(data)
            dataframe = preprocess(data_set)
            MODEL_ADAPTER.w2v_model.update(dataframe)

            results = MODEL_ADAPTER.predict(dataframe, data, THRESHOLD)
            res = json.dumps({"message": "success", "data": results})
            # return res
        except Exception as ex:
            traceback.print_exc()
            res = json.dumps({"message": "error: " + str(ex)})
            # return res
    return res
