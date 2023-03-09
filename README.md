## 字体反爬破解api
一个简易的字体反爬破解api接口 + 简易的token校验。


### 使用说明

    - 复制`config-dev.json`文件为`config.json`并填写自定义的`access_token`；
    - 配置`http-client.env.json`后在`test_main.http`中进行接口调试，其中`access_token`的值跟config.json中的一致；

### docker方式运行

[点击这里查看docker说明](docker/README.md)


### 本地源码运行

- 安装依赖
```shell
pip install -r requirements.txt
```

- 运行
```shell
uvicorn run main:app --reload --host 0.0.0.0 --port 8000
```