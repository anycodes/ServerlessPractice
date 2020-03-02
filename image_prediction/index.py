import uuid, json
import os, base64, random
from imageai.Prediction import ImagePrediction

execution_path = os.getcwd()

prediction = ImagePrediction()
prediction.setModelTypeAsSqueezeNet()
prediction.setModelPath(os.path.join(execution_path, "squeezenet_weights_tf_dim_ordering_tf_kernels.h5"))
prediction.loadModel()


def return_msg(error, msg):
    return_data = {
        "uuid": str(uuid.uuid1()),
        "error": error,
        "message": msg
    }
    print(return_data)
    return return_data


def main_handler(event, context):
    imgData = base64.b64decode(json.loads(event["body"])['pic'])
    fileName = '/tmp/' + "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
    with open(fileName, 'wb') as f:
        f.write(imgData)
    resultData = {}
    predictions, probabilities = prediction.predictImage(fileName, result_count=5)
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        resultData[eachPrediction] = eachProbability
    return return_msg(False, resultData)
