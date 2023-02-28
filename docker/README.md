## 字体反爬破解的api-docker镜像
一个字体反爬破解的api-docker镜像

### 构建api正式包
```shell
docker build . -t samge/font-crack -f docker/Dockerfile
```

### 上传
```shell
docker push samge/font-crack
```

### 运行docker镜像
这里的`/home/samge/docker_data/font-crack/config.json`需要替换为使用者的本地映射路径。
```shell
docker run -d \
--name font-crack \
-v /home/samge/docker_data/font-crack/config.json:/app/config.json \
-p 8233:8000 \
--pull=always \
--restart always \
--memory=1.5G \
samge/font-crack:latest
```
