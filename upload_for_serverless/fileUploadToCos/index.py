import os, json, random, base64, hashlib
import urllib.parse
from qcloud_cos_v5 import CosConfig
from qcloud_cos_v5 import CosS3Client


def getPresignedUrl(event, context):
    print('event', event)
    print('context', context)
    body = json.loads(event['body'])

    # 可以通过客户端传来的token进行鉴权，只有鉴权通过才可以获得临时上传地址
    # 这一部分可以按需修改，例如用户的token可以在redis获取，可以通过某些加密方法获取等
    # 也可以是传来一个username和一个token，然后去数据库中找这个username对应的token是否
    # 与之匹配等，这样会尽可能的提升安全性
    if "key" not in body or "token" not in body or body['token'] != 'mytoken' or "key" not in body:
        return {"url": None}

    # 初始化COS对象
    region = os.environ.get("region")
    secret_id = os.environ.get("TENCENTCLOUD_SECRETID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRETKEY")
    token = os.environ.get("TENCENTCLOUD_SESSIONTOKEN")
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
    client = CosS3Client(config)

    response = client.get_presigned_url(
        Method='PUT',
        Bucket=os.environ.get('bucket_name'),
        Key=body['key'],
        Expired=30,
    )
    return {"url": response.split("?sign=")[0],
            "sign": urllib.parse.unquote(response.split("?sign=")[1]),
            "token": os.environ.get("TENCENTCLOUD_SESSIONTOKEN")}


def uploadToScf(event, context):
    print('event', event)
    print('context', context)
    body = json.loads(event['body'])

    # 可以通过客户端传来的token进行鉴权，只有鉴权通过才可以获得临时上传地址
    # 这一部分可以按需修改，例如用户的token可以在redis获取，可以通过某些加密方法获取等
    # 也可以是传来一个username和一个token，然后去数据库中找这个username对应的token是否
    # 与之匹配等，这样会尽可能的提升安全性
    if "key" not in body or "token" not in body or body['token'] != 'mytoken' or "key" not in body:
        return {"url": None}

    pictureBase64 = body["picture"].split("base64,")[1]
    with open('/tmp/%s' % body['key'], 'wb') as f:
        f.write(base64.b64decode(pictureBase64))
    region = os.environ.get("region")
    secret_id = os.environ.get("TENCENTCLOUD_SECRETID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRETKEY")
    token = os.environ.get("TENCENTCLOUD_SESSIONTOKEN")
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
    client = CosS3Client(config)
    response = client.upload_file(
        Bucket=os.environ.get("bucket_name"),
        LocalFilePath='/tmp/%s' % body['key'],
        Key=body['key'],
    )
    return {
        "uploaded": 1,
        "url": 'https://%s.cos.%s.myqcloud.com' % (
            os.environ.get("bucket_name"), os.environ.get("region")) + body['key']
    }
