import yaml
import json


def getBaseFunctionComponents(functionInformation, functionName=None, tempInputs=None):
    tempInputs = tempInputs if tempInputs else {}
    if functionName:
        tempInputs["name"] = functionName
    if isinstance(functionInformation, dict):
        for eveFunctionKey, eveFunctionValue in functionInformation.items():
            if eveFunctionKey not in ["Events", "Environment", "VpcConfig", "Type", "Role"]:
                tempKey = str.lower(eveFunctionKey[0]) + eveFunctionKey[1:]
                tempInputs[tempKey] = eveFunctionValue
            else:
                if eveFunctionKey == "Environment":
                    if eveFunctionValue and "Variables" in eveFunctionValue:
                        tempEnvironment = {
                            "variables": eveFunctionValue["Variables"]
                        }
                        tempInputs["environment"] = tempEnvironment
                elif eveFunctionKey == "VpcConfig":
                    tempVpcConfig = {}
                    if eveFunctionValue and "SubnetId" in eveFunctionValue:
                        tempSubnetId = eveFunctionValue["SubnetId"]
                        tempVpcConfig["subnetId"] = tempSubnetId
                    if eveFunctionValue and "VpcId" in eveFunctionValue:
                        tempVpcId = eveFunctionValue["VpcId"]
                        tempVpcConfig["vpcId"] = tempVpcId
                    tempInputs["vpcConfig"] = tempVpcConfig
                elif eveFunctionKey == "Events":
                    tempEvents = []
                    if isinstance(eveFunctionValue, dict):
                        for eveEventKey, eveEventValue in eveFunctionValue.items():
                            if isinstance(eveEventValue["Properties"], dict):
                                tempEvent = {}
                                if eveEventValue["Type"] == "APIGW":
                                    tempEvent['apigw'] = {
                                        "name": eveEventKey,
                                        "parameters": {}
                                    }
                                    tempParameter = {}
                                    tempEndpoints = {"path": "/" + functionName}
                                    for eveParameterKey, eveParameterValue in eveEventValue["Properties"].items():
                                        if eveParameterKey == "StageName":
                                            tempParameter["environment"] = eveParameterValue
                                        elif eveParameterKey == "ServiceId" and eveParameterValue:
                                            tempParameter["serviceId"] = eveParameterValue
                                        elif eveParameterKey == "HttpMethod":
                                            tempEndpoints["method"] = eveParameterValue
                                        elif eveParameterKey == "IntegratedResponse":
                                            tempEndpoints["function"] = {"isIntegratedResponse": eveParameterValue}
                                    tempParameter["endpoints"] = [tempEndpoints, ]
                                    tempEvent['apigw']["parameters"] = tempParameter
                                elif eveEventValue["Type"] == "COS":
                                    tempEvent['cos'] = {
                                        "name": eveEventKey,
                                        "parameters": {}
                                    }
                                    tempParameter = {}
                                    for eveParameterKey, eveParameterValue in eveEventValue["Properties"].items():
                                        if eveParameterKey == "Filter":
                                            tempFilter = {}
                                            for eveFilterKey, eveFilterValue in eveParameterValue.items():
                                                tempKey = str.lower(eveFilterKey[0]) + eveFilterKey[1:]
                                                tempFilter[tempKey] = eveFilterValue
                                            tempParameter["filter"] = tempFilter
                                        else:
                                            tempKey = str.lower(eveParameterKey[0]) + eveParameterKey[1:]
                                            tempParameter[tempKey] = eveParameterValue
                                    tempEvent['cos']["parameters"] = tempParameter
                                elif eveEventValue["Type"] == "Timer":
                                    tempEvent['timer'] = {
                                        "name": eveEventKey,
                                        "parameters": {}
                                    }
                                    tempParameter = {}
                                    for eveParameterKey, eveParameterValue in eveEventValue["Properties"].items():
                                        tempKey = str.lower(eveParameterKey[0]) + eveParameterKey[1:]
                                        tempParameter[tempKey] = eveParameterValue
                                    tempEvent['timer']["parameters"] = tempParameter
                                elif eveEventValue["Type"] == "CMQ":
                                    tempEvent['cmq'] = {
                                        "name": eveEventKey,
                                        "parameters": {}
                                    }
                                    tempParameter = {}
                                    for eveParameterKey, eveParameterValue in eveEventValue["Properties"].items():
                                        tempKey = str.lower(eveParameterKey[0]) + eveParameterKey[1:]
                                        tempParameter[tempKey] = eveParameterValue
                                    tempEvent['cmq']["parameters"] = tempParameter
                                elif eveEventValue["Type"] == "CKafka":
                                    tempEvent['ckafka'] = {
                                        "name": eveEventKey,
                                        "parameters": {}
                                    }
                                    tempParameter = {}
                                    for eveParameterKey, eveParameterValue in eveEventValue["Properties"].items():
                                        tempKey = str.lower(eveParameterKey[0]) + eveParameterKey[1:]
                                        tempParameter[tempKey] = eveParameterValue
                                    tempEvent['ckafka']["parameters"] = tempParameter

                                tempEvents.append(tempEvent)
                    if tempEvents:
                        tempInputs["events"] = tempEvents
    return tempInputs


def getFunctionComponents(functionName, function, tempInputs):
    isFunction = False
    if isinstance(function, dict):
        for eveKey, eveValue in function.items():
            if eveKey == "Type" and eveValue == "TencentCloud::Serverless::Function":
                isFunction = True
        if isFunction:
            for eveKey, eveValue in function.items():
                if eveKey == "Type" and eveValue == "TencentCloud::Serverless::Function":
                    continue
                else:
                    tempInputs = getBaseFunctionComponents(eveValue, functionName, tempInputs)
                    serverlessPluginYaml = {
                        "component": '@serverless/tencent-scf',
                        "inputs": tempInputs
                    }
                    return serverlessPluginYaml
        else:
            return False


def getEventPlugin(eventType, eventName, eventSource, deepList=[]):
    tempEvent = {}
    tempEvent[eventType] = {
        "name": eventName,
        "parameters": {}
    }
    tempParameter = {}
    for eveParameterKey, eveParameterValue in eventSource["Properties"].items():
        tempKey = str.lower(eveParameterKey[0]) + eveParameterKey[1:]
        if deepList and eveParameterKey in deepList:
            tempDeepData = {}
            for eveFilterKey, eveFilterValue in eveParameterValue.items():
                tempThisKey = str.lower(eveFilterKey[0]) + eveFilterKey[1:]
                tempDeepData[tempThisKey] = eveFilterValue
            tempParameter[tempKey] = tempDeepData
            continue
        tempParameter[tempKey] = eveParameterValue
    tempEvent[eventType]["parameters"] = tempParameter
    return tempEvent


def getBaseFunctionPlugin(functionInformation, functionName=None, tempInputs=None):
    tempInputs = tempInputs if tempInputs else {}
    if functionName:
        tempInputs["name"] = functionName
    if isinstance(functionInformation, dict):
        for eveFunctionKey, eveFunctionValue in functionInformation.items():
            if eveFunctionKey not in ["Events", "Environment", "VpcConfig", "Type", "Role"]:
                tempKey = str.lower(eveFunctionKey[0]) + eveFunctionKey[1:]
                tempInputs[tempKey] = eveFunctionValue
            else:
                if eveFunctionKey == "Environment":
                    if eveFunctionValue and "Variables" in eveFunctionValue:
                        tempEnvironment = {
                            "variables": eveFunctionValue["Variables"]
                        }
                        tempInputs["environment"] = tempEnvironment
                elif eveFunctionKey == "VpcConfig":
                    tempVpcConfig = {}
                    if eveFunctionValue and "SubnetId" in eveFunctionValue:
                        tempSubnetId = eveFunctionValue["SubnetId"]
                        tempVpcConfig["subnetId"] = tempSubnetId
                    if eveFunctionValue and "VpcId" in eveFunctionValue:
                        tempVpcId = eveFunctionValue["VpcId"]
                        tempVpcConfig["vpcId"] = tempVpcId
                    tempInputs["vpcConfig"] = tempVpcConfig
                elif eveFunctionKey == "Events":
                    tempEvents = []
                    if isinstance(eveFunctionValue, dict):
                        for eveEventKey, eveEventValue in eveFunctionValue.items():
                            if isinstance(eveEventValue["Properties"], dict):
                                tempEvent = {}
                                if eveEventValue["Type"] == "APIGW":
                                    tempEvent = getEventPlugin("apigw", eveEventKey, eveEventValue)
                                elif eveEventValue["Type"] == "COS":
                                    tempEvent = getEventPlugin("cos", eveEventKey, eveEventValue, ["Filter"])
                                elif eveEventValue["Type"] == "Timer":
                                    tempEvent = getEventPlugin("timer", eveEventKey, eveEventValue)
                                elif eveEventValue["Type"] == "CMQ":
                                    tempEvent['cmq'] = getEventPlugin("cmq", eveEventKey, eveEventValue)
                                elif eveEventValue["Type"] == "CKafka":
                                    tempEvent = getEventPlugin("ckafka", eveEventKey, eveEventValue)

                                tempEvents.append(tempEvent)
                    if tempEvents:
                        tempInputs["events"] = tempEvents
    return tempInputs


def getFunctionPlugin(functionName, function, tempInputs):
    isFunction = False
    if isinstance(function, dict):
        for eveKey, eveValue in function.items():
            if eveKey == "Type" and eveValue == "TencentCloud::Serverless::Function":
                isFunction = True
        if isFunction:
            for eveKey, eveValue in function.items():
                if eveKey == "Type" and eveValue == "TencentCloud::Serverless::Function":
                    continue
                else:
                    return getBaseFunctionPlugin(eveValue, functionName, tempInputs)
        else:
            return False


def doComponents(scfYaml):
    try:
        yamlData = yaml.load(scfYaml)
        functions = {}

        if "Globals" in yamlData:
            inputs = getBaseFunctionComponents(yamlData["Globals"]["Function"])

        if isinstance(yamlData['Resources'], dict):
            for eveKey, eveValue in yamlData['Resources'].items():
                for eveNamespaceKey, eveNamespaceValue in eveValue.items():
                    tempInputs = inputs.copy()
                    if eveNamespaceKey == "Type" and eveNamespaceValue == "TencentCloud::Serverless::Namespace":
                        continue
                    tempFunction = getFunctionComponents(eveNamespaceKey, eveNamespaceValue, tempInputs)
                    if tempFunction:
                        functions[eveNamespaceKey] = tempFunction
        return {
            "error": False,
            "result": yaml.safe_dump(functions)
        }
    except:
        return {
            "error": True,
            "result": "Scf Yaml未能正常转换为Serverless Component Yaml"
        }


def doPlugin(scfYaml):
    try:

        yamlData = yaml.load(scfYaml)

        # 获取Provider
        print("获取Provider")
        if "Globals" in yamlData:
            provider = getBaseFunctionPlugin(yamlData["Globals"]["Function"])
        provider["name"] = "tencent"
        provider["credentials"] = "~/credentials"

        # 获取service
        print("获取Service")
        service = "Tencent-Serverless-Framework"

        # 获取插件
        print("获取Plugin")
        plugin = ["serverless-tencent-scf"]

        # 获取函数
        print("获取Function")
        functions = {}

        if isinstance(yamlData['Resources'], dict):
            for eveKey, eveValue in yamlData['Resources'].items():
                for eveNamespaceKey, eveNamespaceValue in eveValue.items():
                    tempInputs = {}
                    if eveNamespaceKey == "Type" and eveNamespaceValue == "TencentCloud::Serverless::Namespace":
                        continue
                    tempFunction = getFunctionPlugin(eveNamespaceKey, eveNamespaceValue, tempInputs)
                    if tempFunction:
                        functions[eveNamespaceKey] = tempFunction

        serverlessJson = {
            "service": service,
            "provider": provider,
            "plugins": plugin,
            "functions": functions
        }

        return {
            "error": False,
            "result": yaml.safe_dump(serverlessJson)
        }
    except Exception as e:
        print(e)
        return {
            "error": True,
            "result": "Scf Yaml未能正常转换为Serverless Plugin Yaml"
        }


def main_handler(event, context):
    print(event)
    try:
        scfYaml = json.loads(event["body"])["yaml"]
    except:
        return {
            "error": True,
            "result": "未正确获得到Yaml信息"
        }

    try:
        if str(event["pathParameters"]["serverless"]).startswith("plugin"):
            return doPlugin(scfYaml)
        elif str(event["pathParameters"]["serverless"]).startswith("components"):
            return doComponents(scfYaml)
    except Exception as e:
        print(e)

    return {
        "error": True,
        "result": "参数错误"
    }
