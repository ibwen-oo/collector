import traceback
from lib.plugins.base import BasePlugin
from lib.utils.response import BaseResponse
from lib.utils.log import cmdb_log

class SYSInfo(BasePlugin):
    def win(self, tgt, handler=None):
        """
        采集windows主机
        :param tgt:
        :param handler:
        :return:
        """
        result = handler.cmd(tgt, "dir")
        return result

    def linux(self, tgt, handler=None):
        """
       采集linux主机
       :param tgt: 目标主机
       :param handler: 采集资源的方式(默认为saltstack)
       :return:
       """
        response = BaseResponse()
        try:
            if self.DEBUG:
                # debug模式,读取文件数据
                pass
            else:
                arg = ("sysinfo", "virtual")
                result = handler.cmd(tgt, "grains.item", arg)
                response.data =  self._parse_data(tgt, result)
        except Exception as e:
            response.status = False
            error_message = traceback.format_exc()
            response.error = error_message
            cmdb_log.logger.error(error_message)
        return response.dict

    def _parse_data(self, tgt, data):
        sys_info = {}
        sys_info["name"] = tgt
        virtual = data[tgt]["virtual"]
        # print(tgt, data)
        for key, value in data[tgt]["sysinfo"].items():
            if key == "interface":
                value.pop("lo")
                sys_info["network"] = self._parse_network(value)
            elif key == "os_info":
                sys_info["uuid"] = value["uuid"]
                sys_info["hostname"] = value["nodename"]
                sys_info["cpu"] = value["num_cpus"]
                sys_info["cpu_model"] = value["cpu_model"]
                sys_info["system"] = value["osfullname"] + " " + value["lsb_distrib_release"]
                sys_info["kernelrelease"] = value["kernelrelease"]
                sys_info["manufacturer"] = value["manufacturer"]
                sys_info["productname"] = value["productname"]
                sys_info["serialnumber"] = value["serialnumber"]
            elif key == "memory":
                sys_info["memory"] = value["mem_total"]

        sys_info.update({"virtual": virtual})
        return sys_info

    def _parse_network(self, interface):
        nic = {}
        for key, value in interface.items():
            nic[key] = {}
            nic[key]["interface"] = key
            nic[key]["hwaddr"] = value.get("hwaddr", None)
            ipv4 = value.get("inet")
            ipaddress = ipv4[0]["address"] if ipv4 else None
            nic[key]["ipaddress"] = ipaddress
            netmask = ipv4[0]["netmask"] if ipv4 else None
            nic[key]["netmask"] = netmask
            nic[key]["state"] = value["up"]

        return nic