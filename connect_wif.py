import snowflake.connector
import os
import urllib.request
import json

# Request OIDC token from GitHub's token endpoint
token_url = os.environ['ACTIONS_ID_TOKEN_REQUEST_URL']
token_bearer = os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN']

req = urllib.request.Request(
    f"{token_url}&audience=[snowflakecomputing.com](https://snowflakecomputing.com)",
    headers={"Authorization": f"bearer {token_bearer}"}
)
with urllib.request.urlopen(req) as resp:
    id_token = json.loads(resp.read())['value']

conn = snowflake.connector.connect(
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    user='GITHUB_PIPELINE_SVC',
    authenticator='WORKLOAD_IDENTITY',
    workload_identity_provider='OIDC',
    token=id_token,
)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM FINANCE_DB.TRANSACTIONS.PAYMENTS")
print(f"✅ Connected without credentials! Payments count: {cur.fetchone()[0]}")
conn.close()
