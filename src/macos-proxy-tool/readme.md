# Script for configuring Wi-Fi proxy servers on MacOS

## Usage
```
bash ~/setup-proxy {socks5_proxy_server} {socks5_proxy_server_port} {http_proxy_server} {http_proxy_server_port} {https_proxy_server} {https_proxy_server_port}
```

You can try as bellows, when you want to set up your proxy servers for Wi-Fi connections on your MacOS
```
bash ~/setup-proxy localhost 23 localhost 24 localhost 25
```

And if you want to clear the settings, just try 
```
bash ~/stop-proxy
```




