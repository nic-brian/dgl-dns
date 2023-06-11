# dgl-dns

This is a Google Cloud Function that creates a generic DNS 'A' record
based on the IP address of the requesting client.

The DNS name is of the form `vmNNN-NNN-NNN-NNN.DOMAIN.TLD`.

`NNN-NNN-NNN-NNN` corresponds to the IP address of the requesting client.

`DOMAIN.TLD` is the domain name to use.

## Requirements

You need a Google Cloud projcet to deploy the function to.

You need `DOMAIN.TLD` either managed by Google Cloud DNS
or managed by Cloudflare.

## Installation

1. Clone this repository.
1. Deploy the function roughly as follows:

```shell
gcloud functions deploy dgl-dns --gen2 --region=us-west1 --runtime=python311 --entry-point=dgl_dns --trigger-http --allow-unauthenticated --update-env-vars=CLOUDFLARE_API_TOKEN=your_cloudflare_api_token,DEFAULT_PROVIDER=cloudflare,DEFAULT_DOMAIN=example.com 
```

`CLOUDFLARE_API_TOKEN` is your Cloudflare API token. This is r
equired if your provider is `cloudflare`.

`DEFAULT_PROVIDER` is either `google` to use Google Cloud DNS 
or `cloudflare` to use Cloudflare DNS. This can be overriden
by the client.

`DEFUALT_DOMAIN` is the default domain to use if the client
does not specify.

## Usage

The client can request a generic DNS 'A' record roughly as follow:

```shell
curl https://cloud_function_url
```

The above command will use `DEFUALT_PROVIDER` and `DEFAULT_DOMAIN` from when
the funciton was deployed. A result of the form `vmNNN-NNN-NNN-NNN.DOMAIN.TLD`
will be returned.

The client can force the provider as follows:

```shell
curl https://cloud_function_url/cloudflare
```

or

```shell
curl https://cloud_function_url/google
```

The client can force the provider and domain as follows:

```shell
curl https://cloud_function_url/cloudflare/someotherdomain.org
```

or

```shell
curl https://cloud_function_url/google/someotherdomain.org
```

The last 2 forms will obviously only work for domains for 
which the Google Cloud Function actuall has responsibility for.



