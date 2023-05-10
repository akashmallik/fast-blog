# Install required packages
```shell
pip install -r requirements.txt
pip install -r requirements_dev.txt
```
or 
```shell
make install
make install-dev
```

# Run server locally
```shell
uvicorn blog.main:app --reload
```
or 
```shell
make run
```
