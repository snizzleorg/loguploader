import nextcloud_client
from dropbox import public_link


nc = nextcloud_client.Client.from_public_link(public_link)
nc.drop_file("ws.zip")
