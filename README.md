# Purpose

This repo provides a (Google) Cloud Function, very primitively implementing Dynamic DNS update API, in order to update (Google) Cloud DNS host A record.

It can be used as a home-made dynamic DNS solution. I created this because I needed to dynamically update the DNS record of my apex domain (so I cannot use a commercial dynamic DNS service because I cannot use CNAME), and also I can keep my fixed/static AAAA (IPv6) record manually.

The files in the repo:

- main.py: implements the Cloud Function
- requirements.txt: needed for the Cloud Function to work
- cloudbuild.yaml: Cloud Build configuration file that deploys the function automatically from a Cloud Source repo

# Installation

I did not test the installation separately, but these are what I have:

- a cloud source repository mirroring this GitHub repo

- a cloud build trigger, using the above repo and using cloudbuild.yaml in the repo. You need to set some permissions/policies for this to work.

The function needs two environment variables, ZONE and PASS. ZONE is the name of zone in Cloud DNS. PASS is checked against the password sent by the dynamic dns update client.

# Using with UDM Pro

It can be directly used with UDM Pro (and possibly other Unifi and Edge routers). Create a dynamic dns config:

- service: dyndns
- hostname: hostname you want to update, write FQDN (no trailing dot)
- username: not used
- password: it should be as same as the value of the PASS environment variable of the cloud function deployed
- server: `<CLOUD_FUNCTION_TRIGGER_URL_WITHOUT_HTTPS>?myip=%i&hostname=%h`

On UDM Pro, you can check the resulting config at `/run/inadyn.conf`. 

# Known Issues

- Cloud Function does not actually check if the DNS record is updated, it only creates the change request.

# References

- https://help.dyn.com/remote-access-api/
