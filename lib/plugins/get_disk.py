import traceback
from lib.plugins.base import BasePlugin
from lib.utils.response import BaseResponse

from lib.utils.log import cmdb_log


class Disk(BasePlugin):

    def win(self, tgt, handler=None):
        pass

    def linux(self, tgt, handler=None):
        response = BaseResponse()
        try:
            if self.DEBUG:
                # debug模式,读取文件数据
                pass
            else:
                arg = "fdisk -l | grep Disk | grep -v 'label type' | grep -v 'identifier'"
                result = handler.cmd(tgt, "cmd.run", (arg, ))
                response.data = self._parse(result, tgt)
                # print(response.data)
        except Exception as e:
            response.status = False
            error_message = traceback.format_exc()
            response.error = error_message
            cmdb_log.logger.error(error_message)
        return response.dict

    def _parse(self, data, tgt):
        disk_data = {}
        filter_tuple = ("mapper", )
        disk_str = data[tgt]
        disk_list = disk_str.split("\n")
        disk_data[tgt] = {}
        for disk in disk_list:
            disk_info = disk.split(",")[0].strip("Disk")
            disk_name, disk_size = disk_info.split(":")
            disk_name = disk_name.strip()
            disk_size = disk_size.strip()
            for filter in filter_tuple:
                if filter not in disk_name:
                    disk_data[tgt][disk_name] = disk_size

        return disk_data