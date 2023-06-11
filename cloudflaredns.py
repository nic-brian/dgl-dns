import CloudFlare

# set up the the Cloudflare API object
_cf = CloudFlare.CloudFlare()

# get the zones
_zones = _cf.zones.get()

# add the resource record if it does not already exist
def add( vhost, domain, target_ip ):
  fqdn = vhost + '.' + domain

  # find the matching zone
  for zone in _zones:
    if domain == zone['name']:
      dns_records = _cf.zones.dns_records.get( zone['id'] )

      # find the matching resource record if it already exists
      for dns_record in dns_records:
        # if we find a match, we are done        
        if fqdn == dns_record['name']:
          return

      # matching resource record not found, so create it
      new_dns_record = {
        'name': vhost,
        'type': 'A',
        'content': target_ip,
        'ttl': 1,
        'proxied': False
      }
      _cf.zones.dns_records.post( zone['id'], data=new_dns_record )
