# Contributions

Before contributing, please set up the pre-commit hooks to reduce
errors and ensure consistency

    pip install -U pre-commit
    pre-commit install

If you run into any issues, you can remove the hooks
with `pre-commit uninstall` and re-run the `pre-commit install` command again.

# python version

The codebase is tested on python3.11.

# configure server

The codebase is tested on an fresh ubuntu 22.04 instance.
```shell
apt update && apt upgrade -y
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.11 python3.11-venv python3.11-dev curl build-essential
```

# ci/cd

You can use the azure devops ci/cd file. Please setup the ssh service endpoint in 
devops and name it: ``ssh_service_server``.

# Install python package manually

```shell
cd /
mkdir services
```

Copy the whole project structure to ``/services``


```shell
python3.11 -m venv /services/cache_warmer/venv
. /services/cache_warmer/venv/bin/activate
pip install /services/cache_warmer
```


# install systemd services

```shell
chmod +x /services/cache_warmer/src/cache_warmer/scheduler.py
cp /services/cache_warmer/src/cache_warmer/cache_warmer.service /etc/systemd/system/cache_warmer.service

```

# service handling

In order to maintain the systemd you can use the following commands on linux:
```shell
sudo systemctl daemon-reload
sudo systemctl enable cache_warmer
sudo systemctl start cache_warmer
sudo systemctl status cache_warmer

sudo systemctl stop cache_warmer
```

# configs
Config files are stored at ``src/cache_warmer/config/``
Under the entry of ``cache_warmer`` you can define multiple cache_warmers.
Each cache_warmer picks up one sitemap that you can create from magento backend.

- ``sitemap_address``: ``str``
    The url to you sitemap.

- ``rate``: ``int``
    The rate parameter handles the asyncio.sleep() after each semaphore requests.
    
- ``semaphore``: ``int``
  The semaphore value for asyncio to limit the max concurrent runs to avoid server downtime.


# logs
To logs can be found here:
```shell
cat /var/log/cache_warmer.log
```

# health checks
You can have health checks that are sent to microsoft teams channel 
made by a webhook.

To configure it please check the ``src/cache_warmer/config/health_check_config.conf``
