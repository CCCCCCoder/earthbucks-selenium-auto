selenium hub使用参考这篇文章
https://i007it.com/2022/05/29/Docker%E7%89%88Selenium%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95/

使用方法：
修改compose.yml中的 public key和 private key   
构建镜像  
```shell
docker compose build
```

运行
```sehll
docker compose -f compose.yml up -d 
```