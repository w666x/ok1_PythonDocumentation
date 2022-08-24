# ok1_PythonDocumentation


1. 若有脚本注释更新，切换到docs的上一级，执行
```sh
sphinx-apidoc -o ./docs/source ./BootstrapFilter  EXCLUDE_PATTERN=docs -f
```

2. 切换到docs目录下, 执行
```sh
cd docs
make clean & make html
# 如果文档没有更新，则可直接执行
cd docs
sphinx-build -b singlehtml source/ build/
```


3. 如果需要生成服务的话，执行
```sh
cd build
python3 -m http.server 8890 --cgi
```
或者，直接执行
```sh
cd docs
zip -r ../build.zip ./build/*
# 然后将build.zip下载到window，直接打开即可
```
