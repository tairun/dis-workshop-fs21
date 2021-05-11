# README #

## Prerequisites ##

- Linux Host (preferably Ubuntu 20.04 LTS)
- Docker CE Engine (v...)
- Python 3.6+ & Python 2.7+ for YCSB (available in /usr/env/python)
- Multipass

## How it works

## How to Run

```bash
docker run -d -v $(pwd)/confs/:/opt/aerospike/etc/ --name aerospike -p 3000-3002:3000-3002 aerospike/aerospike-server --config-file /opt/aerospike/etc/aerospike-mem_4G-rf_1.conf

docker exec -it aerospike asinfo -v "namespace/test" >namespace-test.conf

docker stop aerospike && docker rm aerospike

```

## Sources ##

- https://github.com/aerospike/aerospike-docker-swarm#aerospike-docker-swarm
- https://stackoverflow.com/questions/24418815/how-do-i-install-docker-using-cloud-init
- https://gist.github.com/syntaqx/9dd3ff11fb3d48b032c84f3e31af9163
- https://gist.github.com/HighwayofLife/076d3f026642fb14dbaad9f5847bc0ce
- https://discourse.ubuntu.com/t/advantages-of-using-multipass-instead-of-docker-desktop-on-macos/18069
- https://multipass.run/docs/launch-command
