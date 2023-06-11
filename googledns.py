from google.cloud import dns

# set up the Google Cloud DNS API Client
_client = dns.Client()

# get the zones
_zones = _client.list_zones()

# add the resource record if it does not already exist
def add( vhost, domain, target_ip ):
  fqdn = vhost + '.' + domain + '.'

  # find the matching zone
  for zone in _zones:
    if zone.dns_name == domain + '.':
      rrs = zone.list_resource_record_sets()

      # find the matching resource record if it already exists
      for rr in rrs:
        # if we find a match, we are done
        if fqdn == rr.name:
          return

      # matching resource record not found, so create it
      record_set = zone.resource_record_set( fqdn, 'A', 300, [target_ip] )
      changes = zone.changes()
      changes.add_record_set(record_set)
      changes.create()
