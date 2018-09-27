import urllib2
import re

def check_field_loger_online(url):
    status = '{}/status.php'.format(url)
    rqt = urllib2.urlopen(status)
    contents = rqt.read()
    return ("Serial Number" in contents)


def get_status_field_loger(url):
    status = '{}/status.php'.format(url)
    rqt = urllib2.urlopen(status)
    contents = rqt.read()
    if ("Serial Number" in contents):
        contents = contents.replace("Value</th></tr> ", "Value</th></tr>\n")
        contents = contents.split("\n")
        contents.pop()
        contents.pop(0)
        data_status = {}
        for i in contents:
            item = i.replace("<tr><td>", "").replace("</td></tr>", "").replace("\r", "").replace("</td><td>", "|")
            item =item.split("|")
            data_status[item[0]] = item[1]
        return data_status
    return None


def get_meter_field_loger(url):
    channels = '{}/channels.php'.format(url)
    rqt = urllib2.urlopen(channels)
    contents = rqt.read()
    if("GMXR" in contents):
        contents = contents.split("<hr>").pop(-2)
        contents = contents.replace("Logged</th></tr> ", "Logged</th></tr>\n")
        contents = contents.split("\n")
        contents.pop()
        contents.pop(0)
        data_status = {}
        for item in contents:
            item = item.replace("<tr><td>", "").replace("</td></tr>", "").replace("</td><td>", ",").replace(" ", "")\
                .replace("\r", "")
            item = re.sub(r'[^\w+*\[\]/.]*,', '*', item).split("*")
            if "Barometro" in item[1]:
                data_status["Barometro"] = item[2]
            elif "DirVento" in item[1]:
                data_status["DirVento"] = item[2]
            elif "Temperatura" in item[1]:
                data_status["Temperatura"] = item[2]
            elif "Orvalho" in item[1]:
                data_status["Orvalho"] = item[2]
            elif "DirVento" in item[1]:
                data_status["DirVento"] = item[2]
            elif "RH" in item[1]:
                data_status["RH"] = item[2]
            elif "VelVento" in item[1]:
                data_status["VelVento"] = item[2]
            elif "Chuva" in item[1]:
                data_status["Chuva"] = item[2]
            else:
                data_status[item[1]] = item[2]
        return data_status
    return None


if __name__ == "__main__":

    urls = [
        'localhost:8000']
    for ip in urls:
        url = "http://{}".format(ip)
        try:
            if check_field_loger_online(url):
                status = get_status_field_loger(url)
                print("SN: {};\tTAG: {};\tFirmware_Version: {};\tIP: {};".format(
                    status['Serial Number'],
                    status['Tag'],
                    status['Firmware Version'],
                    ip))

        except urllib2.URLError as ex:
            print "msg: {}\tIP: {}".format(ex, ip)

        except Exception as ex:
            print type(ex)
            print ex

