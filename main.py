import functions_framework
from google.cloud import dns

# set up the Google Cloud DNS API Client
client = dns.Client()

# get the last zone
# (should probably modify this to select a particular zone)
zones = client.list_zones()
last_zone = None
for zone in zones:
  last_zone = zone

# Register an HTTP function with the Functions Framework
@functions_framework.http
def dgl_dns(request):
  # identify IP address of requesting client
  target_ip = request.headers.get( 'X-Forwarded-For', '93.184.216.34')

  # construct new virtual hostname
  vhost = 'vm' + target_ip.replace( '.', '-')

  # construct FQDN for virtual host
  fqdn = vhost + '.' + last_zone.dns_name

  # check to see if the RR already exists
  # if it does, then return immediately
  rrs = last_zone.list_resource_record_sets()
  for rr in rrs:
    if fqdn == rr.name:
      return fqdn

  # otherwise, create new RR for virtual host
  record_set = last_zone.resource_record_set( fqdn, 'A', 300, [target_ip] )
  changes = last_zone.changes()
  changes.add_record_set(record_set)
  changes.create()

  # return FQDN of new virtual host
  return fqdn
