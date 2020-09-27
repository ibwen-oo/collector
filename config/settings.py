import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ssh 配置
SSH_PORT = 22
SSH_USER = "root"


# 虚拟机集群管理中心
vCenter = {
    "host": "10.0.6.241",
    "user": "root",
    "password": "huoban@901"
}

# salt api 配置
SALTURL = "http://10.0.6.110:8000"
SALTUSERNAME = "saltapi"
SALTPASSWORD = "123456"

# 定义采集数据的方法,可以是 salt或ssh(暂未实现)
ENGINE = "salt"

# 定义采集数据的可选方法
ENGINE_DICT = {
    "salt": "lib.engine.salt.SaltHandler",
    "ssh": "lib.engine.ssh.SSHHandler",
}

VMWare_ENGINE = {
    "vmapi": "lib.engine.vmware.VMHHandler"
}

# 宿主机
HostCOLLECTOR_CLASS_DICT = {
    "esxi_host": "lib.plugins.vSphereCollector.HostInfoCollector",
}

# 虚拟机
VMCOLLECTOR_CLASS_DICT = {
    "vm_guest": "lib.plugins.vSphereCollector.VirtualMachineCollector",
}

# 定义采集那些数据
PLUGINS_DICT = {
    "sysinfo": "lib.plugins.get_sysinfo.SYSInfo",
    "disk": "lib.plugins.get_disk.Disk",
    # "nic": "lib.plugin.get_nic.NIC",
    # "memory": "lib.plugin.get_memory.Memory",
}

# 是否开启DEBUG模式
DEBUG = False

# 采集的数据发送到API模块
CMDBAPI = "http://127.0.0.1:8000/api/v1/server/"

LOG_NAME = "cmdb.log"
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs")