import os
import functions_framework
import cloudflaredns
import googledns

default_provider = os.environ.get( 'DEFAULT_PROVIDER', 'cloudflare' )
default_domain = os.environ.get( 'DEFAULT_DOMAIN', 'example.com')

providers = {
  'cloudflare' : {
    'add': cloudflaredns.add
  },
  'google' : {
    'add': googledns.add
  }
}

# Register an HTTP function with the Functions Framework
@functions_framework.http
def dgl_dns(request):
  # identify IP address of requesting client
  target_ip = request.headers.get( 'X-Forwarded-For', '93.184.216.34')

  # construct new virtual hostname
  vhost = 'vm' + target_ip.replace( '.', '-')

  # establish DNS service provider and domain
  provider = default_provider
  domain = default_domain
  path_parts = request.path.split( '/' )
  if len(path_parts) > 1:
    if path_parts[1] in providers:
      provider = path_parts[1]
    if len(path_parts) > 2:
      domain = path_parts[2]

  # construct FQDN for virtual host
  # fqdn = vhost + '.' + last_zone.dns_name
  fqdn = vhost + '.' + domain

  # create new RR for virtual host if needed
  providers[provider]['add']( vhost, domain, target_ip)

  # return FQDN of new virtual host
  return fqdn
