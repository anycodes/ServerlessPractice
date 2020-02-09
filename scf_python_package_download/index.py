# -*- coding: utf8 -*-

import json
import shutil
import zipfile
import os
import sys
import subprocess
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

scf_pip_path = "/tmp/scf_pip/"
shutil.copytree(os.getcwd(), scf_pip_path)
python_version = os.environ.get('python')


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
            Prefix="%s_%s" % (python_version, packageInfor)
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

            # pip_path = os.path.join(os.getcwd(), "pip/__main__.py")
            pip_path = os.path.join(scf_pip_path, "pip/")
            os.chdir(pip_path)

            tpath = "/tmp/%s" % (packageName)
            child = subprocess.Popen(
                "%s %s install %s -t %s -i http://pypi.doubanio.com/simple/  --trusted-host pypi.doubanio.com" % (
                sys.executable,
                "__main__.py", packageInfor, tpath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True,
                shell=True)

            error = child.stderr.read()
            output = child.stdout.read()

            print(error.decode("utf-8"))
            print(output.decode("utf-8"))

            if os.listdir("/tmp/%s" % packageName):
                zipDir("/tmp/%s" % packageName, "/tmp/%s.zip" % packageInfor)
                response = client.upload_file(
                    Bucket=bucket_name,
                    LocalFilePath="/tmp/%s.zip" % packageInfor,
                    Key="%s_%s.zip" % (python_version, packageInfor),
                )
                print(response['ETag'])
                response = client.get_presigned_download_url(
                    Bucket=bucket_name,
                    Key="/%s_%s.zip" % (python_version, packageInfor)
                )
                return {
                    "error": False,
                    "result": str(response)
                }
            else:
                return {
                    "error": True,
                    "result": error.decode("utf-8")
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
