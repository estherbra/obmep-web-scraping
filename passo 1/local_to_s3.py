
from airflow.hooks.S3_hook import S3Hook

def local_to_s3():
    s3_hook = S3Hook()
    s3_hook.load_file('df_obmep.parquet.gzip', key='pq/obmep.pq', bucket_name='1sti-bucket', replace=True)