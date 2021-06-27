import os
from google.cloud.dns.client import Client

zone_name = os.environ['ZONE']

def main(request):

    hostname = request.args.get('hostname', None)
    myip = request.args.get('myip', None)

    if hostname is None:
        return f'nohost'

    if myip is None:
        return f'nochg'

    print(hostname)
    print(myip)

    cli = Client()
    zone = cli.zone(zone_name)
    # rr has trailing dot
    hostname = hostname + '.'
    rr = zone.resource_record_set(hostname, 'A', 60, [myip])
    changes = zone.changes()
    changes.delete_record_set(rr)
    changes.add_record_set(rr)
    changes.create()

    return f'good ' + myip
