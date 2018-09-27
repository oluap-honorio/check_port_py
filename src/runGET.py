import urllib2
import re

''' POST
url = 'http://www.someserver.com/cgi-bin/register.cgi'
values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'Python' }

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
'''
'''
data = {}
data['name'] = 'Somebody Here'
data['location'] = 'Northampton'
data['language'] = 'Python'
url_values = urllib.urlencode(data)
print url_values  # The order may differ.
name=Somebody+Here&language=Python&location=Northampton
url = 'http://www.example.com/example.cgi'
full_url = url + '?' + url_values
data = urllib2.urlopen(full_url)

'''


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
    url = 'http://localhost:8000'

    lista = get_status_field_loger(url)
    lista = get_meter_field_loger(url)
    for item in lista:
        print "'{}' => {}".format(item, lista[item])

    print check_field_loger_online(url)
