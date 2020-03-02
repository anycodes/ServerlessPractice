# 我的API

## 概述
我的API是一系列有趣的或者实用API，这些API的共同点都是基于Serverless Framework来构造的。
* 体验地址：http://serverless.0duzhan.com

## APIs

基础地址：http://service-8d3fi753-1256773370.bj.apigw.tencentcs.com/release

* [获取用户IP地址](#获取用户IP地址)
* [新年为头像加装饰](#新年为头像加装饰)
* [圣诞节为头像戴圣诞帽](#圣诞节为头像戴圣诞帽)
* [图像内容识别](#图像内容识别)

实践类文章地址

* [20行代码：Serverless架构下用Python轻松搞定图像分类](https://zhuanlan.zhihu.com/p/110339482)
* [如何在Serverless上部署SCFCLI/VSCode插件生成的项目](https://zhuanlan.zhihu.com/p/110155146)
* [ServerlessComponent：全局变量组件和单独部署方法](https://zhuanlan.zhihu.com/p/110071590)
* [Serverless架构的无状态性究竟是什么](https://zhuanlan.zhihu.com/p/110071540)
* [用Serverless怎么实现文件上传（附代码）](https://zhuanlan.zhihu.com/p/110071452)
* [传统的Web框架如何部署在Serverless架构上（以Flask为例）](https://zhuanlan.zhihu.com/p/110071391)
* [Serverless架构下Python语言实现一个基于人工智能的相册小程序](https://zhuanlan.zhihu.com/p/110071256)
* [【公众号开发】用Serverless快速上手微信公众号开发](https://zhuanlan.zhihu.com/p/110070824)
* [【公众号开发】人工智能让我们的公众号活起来](https://zhuanlan.zhihu.com/p/110070755)
* [Serverless架构与资源评估：性能与成本探索帽](https://zhuanlan.zhihu.com/p/110070567)
* [我是如何为Serverless配置内存和超时时间的](https://zhuanlan.zhihu.com/p/110070487)
* [Serverless架构如何获取用户IP和归属地运营商](https://zhuanlan.zhihu.com/p/110070407)
* [传统的Web框架如何部署在Serverless架构上（以Flask为例）](https://zhuanlan.zhihu.com/p/110070046)
* [从SCFCLI/SCF VSCode迁移过渡到Serverless Framework](https://zhuanlan.zhihu.com/p/109926801)
* [如何为Serverless架构做了一个Django的Component](https://zhuanlan.zhihu.com/p/109926704)
* [用腾讯云Serverless你要知道他们两个的区别](https://zhuanlan.zhihu.com/p/109926610)
* [基于Serverless的图书查询APP的实现](https://zhuanlan.zhihu.com/p/109926497)
* [云计算：Serverless Framework与Serverless CLI](https://zhuanlan.zhihu.com/p/109926315)
* [你好，Serverless Framework](https://zhuanlan.zhihu.com/p/109926172)
* [Serverless: 你好，世界](https://zhuanlan.zhihu.com/p/109925923)
* [圣诞节：让Serverless送你一顶圣诞帽](https://zhuanlan.zhihu.com/p/109925775)
* [新年到：Serverless帮你做贺卡](https://zhuanlan.zhihu.com/p/109925609)
* [新年到：让Serverless给你头像加点装饰](https://zhuanlan.zhihu.com/p/109925202)
* [基于Serverless架构的Python Blog开发(原生开发与Flask框架结合)](https://zhuanlan.zhihu.com/p/109886060)
* [【公众号开发】用Serverless实现公众号图文搜索功能](https://zhuanlan.zhihu.com/p/109843939)


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

### 图像内容识别

接口路径：/image_prediction

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
        {
            "cheetah": 83.12643766403198, 
            "Irish_terrier": 2.315458096563816, 
            "lion": 1.8476998433470726, 
            "teddy": 1.6655176877975464, 
            "baboon": 1.5562783926725388
        }
    }
}
```
