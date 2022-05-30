# 读取配置项的指定内容
import configparser


def read(path, section, option):
    conf = configparser.ConfigParser()
    conf.read(path)
    value = conf.get(section, option)
    print(value)
    return value
