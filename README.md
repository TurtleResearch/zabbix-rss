A tiny self-serving RSS wrapper for Zabbix API. Hosts an RSS feed for zabbix trigger events.
Requires 
    Python 2.7
    web.py http://webpy.org/ (easy_install web.py)
    zabbix-api https://github.com/gescheit/scripts/tree/master/zabbix (pip install zabbix-api)

Usage:
    "python daemon.py -l http://your.zabbix.null -u zabbix_user -p zabbix_password"  will start a server listening on 0.0.0.0:8080
    
    Invoke "python daemon.py -h" for additional arguments.