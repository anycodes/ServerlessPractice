# -*- coding:utf-8 -*-

import urllib.request
import json
import uuid


def return_msg(error, msg):
    return_data = {
        "uuid": str(uuid.uuid1()),
        "error": error,
        "message": msg
    }
    print(return_data)
    return return_data


def get_ip_addr(ip):
    url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=%s&co=&resource_id=6006" % ip
    ip_data = json.loads(urllib.request.urlopen(url=url).read().decode("gbk"))
    if ip_data["data"] and len(ip_data["data"]) > 0:
        return ip_data["data"][0]["location"]
    else:
        return False


def main_handler(event, context):
    try:
        try:
            user_ip = json.loads(event["body"])["ip"]
        except:
            user_ip = event["requestContext"]["sourceIp"]

        location = get_ip_addr(user_ip)
        if location:
            return return_msg(False, {"ip": user_ip, "location": location})
        else:
            return return_msg(True, "未能正确获得到IP地址")
    except Exception as e:
        print(e)
        return return_msg(True, "内部错误")


def test():
    event = {
        "requestContext": {
            "serviceId": "service-f94sy04v",
            "path": "/test/{path}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "identity": {
                "secretId": "abdcdxxxxxxxsdfs"
            },
            "sourceIp": "14.17.22.34",
            "stage": "release"
        },
        "headers": {
            "Accept-Language": "en-US,en,cn",
            "Accept": "text/html,application/xml,application/json",
            "Host": "service-3ei3tii4-251000691.ap-guangzhou.apigateway.myqloud.com",
            "User-Agent": "User Agent String"
        },
        "body": "{\"test\":\"body\"}",
        "pathParameters": {
            "path": "value"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headerParameters": {
            "Refer": "10.0.2.14"
        },
        "stageVariables": {
            "stage": "release"
        },
        "path": "/test/value",
        "queryString": {
            "foo": "bar",
            "bob": "alice"
        },
        "httpMethod": "POST"
    }
    print(main_handler(event, None))


if __name__ == "__main__":
    test()