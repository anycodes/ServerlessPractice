# 我的API

## 概述
我的API是一系列有趣的或者实用API，这些API的共同点都是基于Serverless Framework来构造的。
* 体验地址：http://serverless.0duzhan.com

## APIs

基础地址：http://service-8d3fi753-1256773370.bj.apigw.tencentcs.com/release

* [获取用户IP地址](#获取用户IP地址)
* [新年为头像加装饰](#新年为头像加装饰)
* [圣诞节为头像戴圣诞帽](#圣诞节为头像戴圣诞帽)

实践类文章地址

* [【实践】基于Serverless的人工智能相册小程序](https://zhuanlan.zhihu.com/p/102935668)
* [【实践】基于Serverless的图书查询APP的实现](https://zhuanlan.zhihu.com/p/101572333)
* [新年到：Serverless帮你做贺卡](https://zhuanlan.zhihu.com/p/100872800)
* [新年到：让Serverless给你头像加点装饰](https://zhuanlan.zhihu.com/p/100432264)
* [我的API系列：获取用户IP和归属地运营商](https://zhuanlan.zhihu.com/p/100326243)
* [我是如何为Serverless配置内存和超时时间的](https://zhuanlan.zhihu.com/p/100253577)
* [腾讯云Serverless架构安装Python依赖的小工具（包括对外的API，基于SCF）](https://zhuanlan.zhihu.com/p/99890261)
* [SCF CLI/VSCODE Yaml 快速转换为Serverless Plugin Yaml](https://zhuanlan.zhihu.com/p/99718289)
* [SCFCLI/VSCODE插件Yaml快速转换为Serverless Components Yaml](https://zhuanlan.zhihu.com/p/99475957)
* [圣诞节：让Serverless送你一顶圣诞帽](https://zhuanlan.zhihu.com/p/99275301)
* [Serverless架构与资源评估：性能与成本探索](https://zhuanlan.zhihu.com/p/99130419)
* [你好，Serverless Framework](https://zhuanlan.zhihu.com/p/98596244)
* [Serverless: 你好，世界](https://zhuanlan.zhihu.com/p/95754819)

### 获取用户IP地址

如果填写入参ip，会返回填写ip对应的信息，否则会返回客户端的ip相关信息。

路径：/get_user_ip

入参：

| 参数 | 必选 | 类型 |  描述 |
| ---- | ---- | ------ | ---- | 
| ip | 否 | String | IP地址 |

出参格式：

```text
{
    "uuid": "51ef795c-2b77-11ea-9704-0242cb007103",
    "error": false,
    "message": {
        "ip": "192.168.1.1",
        "location": "本地局域网"
    }
}
```

### 新年为头像加装饰

接口路径：/new_year_add_photo_decorate

入参：

| 参数 | 必选 | 类型 |  描述 |
| ---- | ---- | ------ | ---- | 
| pic | 是 | String | 图片base64 |
| base | 是 | String | 装饰编号 |

出参格式：

```text
{
    "uuid": "9df88d10-2bbe-11ea-ad59-0242cb007102",
    "error": false,
    "message": {
        "picture": "生成后图像的base64编码"
    }
}
```
base对应关系 [文件名就是编号](/new_year_add_photo_decorate/base)


### 圣诞节为头像戴圣诞帽

接口路径：/add_christmas_hat

入参：

| 参数 | 必选 | 类型 |  描述 |
| ---- | ---- | ------ | ---- | 
| pic | 是 | String | 图片base64 |

出参格式：

```text
{
    "uuid": "9df88d10-2bbe-11ea-ad59-0242cb007102",
    "error": false,
    "message": {
        "picture": "生成后图像的base64编码"
    }
}
```