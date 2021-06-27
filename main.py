import os
import base64
from google.cloud.dns.client import Client

zone_name = os.environ['ZONE']
correct_pass = os.environ['PASS']

def main(request):

    auth = request.headers.get('Authorization', None)
    if auth is None:
        return f'badauth'

    if not auth.startswith('Basic'):
        return f'badauth'

    auth = auth[5:].strip()
    unpw = base64.standard_b64decode(auth.encode('ASCII')).split(':')

    print(unpw)

    if unpw[1] != correct_pass:
        return f'badauth'

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
    found = None
    for item in zone.list_resource_record_sets():
        if item.name == hostname and item.record_type == 'A':
            found = item
            break

    if found is None:
        return f'nohost'

    changes = zone.changes()
    changes.delete_record_set(found)
    rr = zone.resource_record_set(hostname, 'A', 60, [myip])
    changes.add_record_set(rr)
    changes.create()

    # not checking if changes are applied

    return f'good ' + myip
