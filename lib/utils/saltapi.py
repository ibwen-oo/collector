#!/bin/env python3

import copy
import requests
from requests.packages import urllib3

from config import settings

# 关闭ssl报警信息
urllib3.disable_warnings()


class SaltAPI():

    def __init__(self, url, username, password, eauth):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__eauth = eauth
        self.__base_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.__base_data = dict(
            username=self.__username,
            password=self.__password,
            eauth=self.__eauth
        )
        self.__token = self._get_token()
        self.__headers_token = {'X-Auth-Token': self.__token}
        self.__headers_token.update(self.__base_headers)

    # 获取token
    def _get_token(self):
        params = copy.deepcopy(self.__base_data)
        try:
            response = requests.post(url=self.__url + '/login', verify=False, headers=self.__base_headers, json=params)
            ret_json = response.json()
            token = ret_json["return"][0]["token"]
            return token
        except Exception as ErrorMsg:
            print(ErrorMsg)

    # 发送 post 请求
    def __post(self, **kwargs):
        try:
            response = requests.post(url=self.__url, verify=False, headers=self.__headers_token, **kwargs)
            ret_code, ret_data = response.status_code, response.json()
            return (ret_code, ret_data)
        except Exception as ErrorMsg:
            print(ErrorMsg)
            exit()

    def list_all_key(self):
        """
        获取所有认证和未认证的salt主机
        :return:
        """
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        response = self.__post(json=params)
        accepted_minions = response[1]['return'][0]['data']['return']['minions']
        unaccepted_minions = response[1]['return'][0]['data']['return']['minions_pre']
        return accepted_minions, unaccepted_minions

    def run(self, params):
        """
        远程执行salt通用接口,需要自定义参数字典.
        格式如下:
            params = {
                'client': 'local',
                'fun': 'grains.item',
                'tgt': '*',
                'arg': ('os', 'id', 'host' ),
                'kwarg': {},
                'expr_form': 'glob',
                'timeout': 60
            }
         """
        response = self.__post(json=params)
        return response[1]['return'][0]

    def process(self, tgt, fun, *args):
        """采集服务器资源"""
        arg = args[0] if args else ()
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, "arg": arg}
        response_code, response_content = self.__post(json=params)
        if response_code == 200:
            content = response_content["return"][0]
            return content
        else:
            print("{} 命令执行失败".format(tgt))

    def _parse_data(self, tgt, data):
        sys_info = {}
        sys_info["name"] = tgt
        for key, value in data[tgt]["sysinfo"].items():
            # print("key: {}, value: {}".format(key, value))
            if key == "interface":
                value.pop("lo")
                sys_info["network"] = self._parse_network(value)
            elif key == "os_info":
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


sapi = SaltAPI(url=settings.SALTURL, username=settings.SALTUSERNAME, password=settings.SALTPASSWORD, eauth="pam")
