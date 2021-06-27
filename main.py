import os
import base64
from google.cloud.dns.client import Client

zone_name = os.environ['ZONE']

def main(request):

    auth = request.headers.get('Authorization', None)
    if auth is None:
        return f'badauth'

    if not auth.startswith('Basic'):
        return f'badauth'

    auth = auth[5:].strip()
    unpw = base64.standard_b64decode(auth)

    print(unpw)

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
    item = None
    for item in zone.list_resource_record_sets():
        if item.name == hostname and item.record_type == 'A':
            found = item
            break
    changes = zone.changes()
    if found:
        changes.delete_record_set(found)
    rr = zone.resource_record_set(hostname, 'A', 60, [myip])
    changes.add_record_set(rr)
    changes.create()

    return f'good ' + myip
