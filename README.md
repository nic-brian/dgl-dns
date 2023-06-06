# dgl-dns

This is a Google Cloud Function which creates a generic DNS 'A' resource record
based on the IP address of the client.

The function is typically deployed as follows:

```bash
gcloud functions deploy dgl-dns --gen2 --region=us-west1 --runtime=python311 --entry-point=dgl_dns --trigger-http --allow-unauthenticated
```
