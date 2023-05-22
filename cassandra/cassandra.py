from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config= {
  'secure_connect_bundle': 'secure-connect-bety.zip'
}
auth_provider = PlainTextAuthProvider("jxbiZCoHJMGchSaeNztzfbTn", "6y9NvWWsP4jDRFCWZZ72XU8cBrFuY5-qgLzNZQfW3rYwchFtT4G-Arlxni23Sy8DXIrOnhksAeMWzjS4KovDq_BZiuKq_Mc2z-TsT+wL,BdqFB15gdc,kyJWAz_.KfZ6")
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")