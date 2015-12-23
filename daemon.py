import web
from datetime import datetime
from zabbix_api import ZabbixAPI
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--url', help="Zabbix web URL", required=True)
parser.add_argument('-s', '--host', help="Host for this server. ex: 0.0.0.0:8080", required=False,
                    default="0.0.0.0:8080")
parser.add_argument('-u', '--user', help="Zabbix user name", required=True)
parser.add_argument('-p', '--password', help="Zabbix password", required=True)
parser.add_argument("-c", "--count", help="Max amount of items to be shown", default=50)
parser.add_argument("-r", "--priority",
                    help="Minimum trigger priority. Only trigger events equal to or above this will show up. "
                         "0 - (default) not classified 1 - information 2 - warning 3 - average 4 - high 5 - disaster.",
                    default=0, type=int)
args = parser.parse_args()
urls = (
    '/', 'root'
)
render = web.template.render('.')


class Record:
    def __init__(self, title, body, link, date, id):
        self.title = title
        self.body = body
        self.link = link
        self.date = date
        self.id = id


def makeRecord(zabbix, event):
    try:
        if event["object"] == '0':
            link = args.url
            if not link.endswith("/"):
                link += "/"
            robj = event["relatedObject"]
            host = ", ".join([x["host"] for x in event["hosts"]])
            if int(robj["priority"]) < int(args.priority): return None
            description = robj["description"]
            if len(description) == 0:
                description = "(No trigger description, ID: " + robj["triggerid"]
            title = (description.replace("{HOST.NAME}", host)) if "{HOST.NAME}" in description else (
                host + ": " + description)
            body = robj["comments"] + "<br/>"
            body += "Status: " + ("OK" if event["value"] == '0' else "PROBLEM") + "<br/>"
            link += "tr_events.php?triggerid=" + robj["triggerid"] + "&eventid=" + event["eventid"]
            body += "At: " + str(datetime.fromtimestamp(float(event["clock"]))) + "<br/>"
            body += "Acknowledged: " + event["acknowledged"] + "<br/>"
        else:
            print "Unsupported event: " + str(event)
            return None
    except Exception, e:
        print str(e)
        return None
    return Record(title, body, link, datetime.fromtimestamp(float(event["clock"])), event["eventid"])


class root:
    def GET(self):
        web.header('Content-Type', 'application/xml')
        zabbix = ZabbixAPI(server=args.url)
        zabbix.login(args.user, args.password)
        events = zabbix.event.get(
                {"limit": 100, "sortfield": "clock", "sortorder": "DESC", "extendoutput": True, "selectHosts": "extend",
                 "selectRelatedObject": "extend"})
        records = [x for x in [makeRecord(zabbix, e) for e in events] if x is not None]
        return render.rss(records=records, date=datetime.now() if len(records) == 0 else records[-1].date)


if __name__ == "__main__":
    web.config.debug = False
    app = web.application(urls, globals())
    sys.argv = [sys.argv[0]]  # hack away the args so web.py can start...
    app.run()
