# gopygo


```bash
$ pip install -r requirements.txt
$ python client.py
```

### Load server on robot startup

```bash
$ ssh pi@dex.local
$ sudo cp rpc-server.sh /etc/init.d/rpc-server
```

```bash
$ sudo /etc/init.d/rpc-server start
$ sudo /etc/init.d/rpc-server status
$ sudo /etc/init.d/rpc-server restart
$ sudo /etc/init.d/rpc-server stop
```

* `/var/log/rpcserver.log` logs
* `/var/run/rpcserver.pid` pid file

### Read more
* [Using XML RPC to control your GoPiGo](https://bmwlog.pp.ua/post/using-xml-rpc-to-control-your-gopigo)
