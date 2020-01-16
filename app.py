from flask import Flask, request
try:
    import ujson as json
except Exception:
    import json

app = Flask(__name__)

import os
import re
import traceback
from sklearn.externals import joblib
from pandas.io.json import json_normalize
from anomaly_detector.config import Configuration
from anomaly_detector.adapters import SomStorageAdapter, SomModelAdapter

CONFIGURATION_PREFIX = "LAD"
config_yaml = "/home/my_lad/config_files/.env_cmn_log_fmt_config.yaml" 

config = Configuration(prefix=CONFIGURATION_PREFIX, config_yaml=config_yaml)
storage_adapter = SomStorageAdapter(config)
model_adapter = SomModelAdapter(storage_adapter)
model_adapter.load_w2v_model()
model_adapter.load_som_model()
mean, threshold = model_adapter.set_threshold()


@app.route("/log/anomalydetector",
           methods=["POST", "GET"])
def r_forecast():
    if request.method == "GET":
        return "Hello World"
    if request.method == "POST":
    
        def clean_message(line):
            """Remove all none alphabetical characters from message strings."""
            return "".join(
                re.findall("[a-zA-Z]+", line)
            )  # Leaving only a-z in there as numbers add to anomalousness quite a bit

        def preprocess(data):
            """Provide preprocessing for the data before running it through W2V and SOM."""
            def to_str(x):
                """Convert all non-str lists to string lists for Word2Vec."""
                ret = " ".join([str(y) for y in x]) if isinstance(x, list) else str(x)
                return ret

            for col in data.columns:
                if col == "message":
                    data[col] = data[col].apply(clean_message)
                else:
                    data[col] = data[col].apply(to_str)

            data = data.fillna("EMPTY")
                
        try:
            request_data: dict = json.loads(request.data)
            df = request_data.get("data", None)
            data = [] 
            if df == None  or len(df) == 0:
                return json.dumps({"message": "error: No log data"})
                
            for message_field in df:
                data.append({"message": message_field})
            data_set = json_normalize(data)
            preprocess(data_set)
            dataframe, raw_data = data_set, data
            
            model_adapter.w2v_model.update(dataframe)
            """
            try:
                model_adapter.w2v_model.save(model_adapter.storage_adapter.W2V_MODEL_PATH)
            except ModelSaveException as ex:
                ## logging.error("Failed to save W2V model: %s" % ex)
                print("Failed to save W2V model: %s" % ex)
                raise 
            """
            results = model_adapter.predict(dataframe, data, threshold)
            return json.dumps({"message": "success", "data": results})

        except Exception as e:
            traceback.print_exc()
            return json.dumps({"message": "error: " + str(e)})


