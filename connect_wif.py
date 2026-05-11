import snowflake.connector
import os

conn = snowflake.connector.connect(
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    user='GITHUB_PIPELINE_SVC',
    authenticator='WORKLOAD_IDENTITY',
    workload_identity_provider='OIDC',
)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM FINANCE_DB.TRANSACTIONS.PAYMENTS")
print(f"✅ Connected without credentials! Payments count: {cur.fetchone()[0]}")
conn.close()
