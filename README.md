# 腾讯云API网关日志保存

以天为单位保存腾讯云API网关日志。可选上传到腾讯云COS。

## 需要的权限策略

`QcloudAPIGWReadOnlyAccess`（用于获取日志）和`QcloudCOSDataWriteOnly`（用于保存获取到的日志到COS）。

## 本地命令行程序

命令行程序为`main.py`，需要在环境变量`TENCENTCLOUD_SECRETID`和`TENCENTCLOUD_SECRETKEY`中提供可访问需要的权限策略的用户的secret id和secret key。

| 参数 | 可选 | 内容 |
|-----|-----|-----|
| -r, --region     | 否 | 目标API网关和（如上传到COS）bucket的所在区域 |
| -s, --service-id | 否 | 目标API网关的service id |
| -p, --path       | 否 | 保存日志的路径（本地路径或bucket路径） |
| -b, --bucket     | 是 | （如上传到COS）上传到bucket的名称 |
| -d, --date       | 是 | （如要指定日期）要保存哪一天的日志，日期格式为Y-m-d |

## 部署为云函数

部署前先创建自定义角色`scf-apigw-save-log`并允许需要的权限策略。

确保本地环境配置好python3和pip后，将`requirements.txt`复制到一个空文件夹，并在该文件夹下运行`pip install -r requirements.txt -t .`，然后将整个文件夹的内容打包为一个zip文件，上传为一个层，起名为`apigw-save-log-deps`，环境设置为Python 3.7。

在`serverless.yml`中填写空缺的组件实例名称、云函数所在区域以及四个环境变量（内容同命令行程序参数，`--path`对应`FILE_PATH`），并将其以`serverless.yml`的文件名另存为到一个空文件夹。将`api.py` `proc.py` `scf.py`三个所需文件复制到该文件夹。确保安装好腾讯云serverless cli（`npm i -g serverless`）后，在该文件夹下运行`serverless deploy`以部署函数。部署完成后记得到控制台绑定前面建立的`apigw-save-log-deps`层。

默认情况下这个云函数每天凌晨1点收集前一天的日志并上传到COS。这个云函数不会读取触发事件的payload，每次执行它都会收集前一天的日志。
