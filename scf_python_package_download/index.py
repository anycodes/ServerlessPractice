import pip._internal.main
import json
import os
import zipfile
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = ''  # 替换为用户的 secretId
secret_key = ''  # 替换为用户的 secretKey
region = 'ap-shanghai'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)
bucket_name = 'serverless-cache-1256773370'


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


def main_handler(event, context):
    try:
        packageName = json.loads(event["body"])["name"]
    except:
        packageName = None

    try:
        packageVersion = json.loads(event["body"])["version"]
    except:
        packageVersion = None

    if packageName:
        if packageVersion:
            packageInfor = "%s==%s" % (packageName, packageVersion)
        else:
            packageInfor = "%s" % (packageName)

        response = client.list_objects(
            Bucket=bucket_name,
            Prefix="python3_%s" % packageInfor
        )

        if 'Contents' in response and response['Contents'] and len(response['Contents']) > 0:
            for eve in response['Contents']:
                response = client.get_presigned_download_url(
                    Bucket=bucket_name,
                    Key=eve['Key']
                )
                return {
                    "error": False,
                    "result": str(response)
                }

        try:
            os.makedirs("/tmp/%s" % packageName)
        except:
            pass
        try:
            install_list = ["install", packageInfor, "-t", "/tmp/%s" % (packageName), "-i",
                            "http://pypi.doubanio.com/simple/", "--trusted-host", "pypi.doubanio.com"]
            print(install_list)
            pip._internal.main.main(install_list)
            if os.listdir("/tmp/%s" % packageName):
                zipDir("/tmp/%s" % packageName, "/tmp/%s.zip" % packageInfor)
                response = client.upload_file(
                    Bucket=bucket_name,
                    LocalFilePath="/tmp/%s.zip" % packageInfor,
                    Key="python3_%s.zip" % packageInfor,
                )
                print(response['ETag'])
                response = client.get_presigned_download_url(
                    Bucket=bucket_name,
                    Key="/python3_%s.zip" % packageInfor
                )
                return {
                    "error": False,
                    "result": str(response)
                }
            else:
                return {
                    "error": True,
                    "result": "依赖安装失败"
                }
        except Exception as e:
            print(e)
            return {
                "error": True,
                "result": str(e)
            }
    else:
        return {
            "error": True,
            "result": "未获得到包名，请检查输入"
        }
