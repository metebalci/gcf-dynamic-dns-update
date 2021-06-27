def main(request):

    hostname = request.args.get('hostname', None)
    myip = request.args.get('myip', None)

    print(hostname)
    print(myip)

    return f'nochg'
