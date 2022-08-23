# ok1_PythonDocumentation


1. 若有脚本注释更新，切换到doc的上一级，执行
sphinx-apidoc -o ./doc/source ./BootstrapFilter  EXCLUDE_PATTERN=docs -f

i2. 切换到doc目录下, 执行
cd doc
make clean & make html

3. 如果需要生成服务的话，执行
cd build
python3 -m http.server 8890 --cgi
