import functions_framework
from google.cloud import dns

# Register an HTTP function with the Functions Framework
@functions_framework.http
def dgl_dns(request):
  # set up the Google Cloud DNS API Client
  client = dns.Client()

  # get the last zone
  # (should probably modify this to select a particular zone)
  zones = client.list_zones()
  last_zone = None
  for zone in zones:
    last_zone = zone

  # identify IP address of requesting client
  target_ip = request.headers.get( 'X-Forwarded-For', '93.184.216.34')

  # construct new virtual hostname
  vhost = 'vm' + target_ip.replace( '.', '-')

  # construct FQDN for new virtual host
  fqdn = vhost + '.' + last_zone.dns_name

  # create RR for new virtual host
  record_set = last_zone.resource_record_set( fqdn, 'A', 300, [target_ip] )
  changes = zone.changes()
  changes.add_record_set(record_set)
  changes.create()

  # return FQDN of new virtual host
  return fqdn
