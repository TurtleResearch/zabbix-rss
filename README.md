A tiny self-serving RSS wrapper for Zabbix API. Hosts an RSS feed for zabbix trigger events.

## Requires 

Python 2.7

    web.py http://webpy.org/ easy_install web.py
    zabbix-api https://github.com/gescheit/scripts/tree/master/zabbix (pip install zabbix-api)

## Usage:

    python daemon.py -l http://your.zabbix.null -u zabbix_user -p zabbix_password
Will start a server listening on 0.0.0.0:8080.
    
# Optional arguments:

    -h, --help                  show this help message and exit
    -l URL, --url URL           Zabbix web URL
    -s HOST, --host HOST        Host for this server. ex: 0.0.0.0:8080
    -u USER, --user USER        Zabbix user name
    -p PASSWORD, --password     PASSWORD  Zabbix password
    -c COUNT, --count COUNT     Max amount of items to be shown
    -r PRIORITY, --priority PRIORITY
                            Minimum trigger priority. Only trigger events equal to
                            or above this will show up. 0 - (default) not
                            classified 1 - information 2 - warning 3 - average 4 -
                            high 5 - disaster.
