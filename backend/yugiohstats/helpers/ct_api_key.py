


def get_auth_headers():
    ct_api_key = 'eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJjYXJkdHJhZGVyLXByb2R1Y3Rpb24iLCJzdWIiOiJhcHA6MTA1OTQiLCJhdWQiOiJhcHA6MTA1OTQiLCJleHAiOjQ4NzMyNTE4NDAsImp0aSI6IjEwN2ZhZGIyLTIzM2MtNDc4Yy1hYmUzLTY5NzYwNmU3MTkzZiIsImlhdCI6MTcxNzU3ODI0MCwibmFtZSI6Ik9saWp3b29kIEFwcCAyMDI0MDYwNTEwMDM0MiJ9.mfGV7emliqyZL4-smLwN-RQ6pgOKb7AZ6QwlC9dnlh6YNm0R5gduG0bv_yjurwLHdftTFUGzUs_6III9bFMPbWgGUUavnmBAryM6eQPS-wEVq7m9PdrQwGbkjB_BFxFuOVaTsbDNAqYo9EnsLfLRr6TbV5zzWaIFylDbrlw4fTjit900wfdBlY4bqpJZZ-O9LzF5Lx2B0qHvIZBCrpE7kL_iRiwincseA5TI6x8iWhp4AvYfRxh-MruA_VWP8idRs4aJzoPx5RT3dgXKbIL3kpzq8XocD71y0XzL6vSFqCJALzFe0RTsfJuSowqiSB80ST0oZ_3zDVCebA-okrlfcg'
    dict = {'Authorization': f'Bearer {ct_api_key}'}
    return dict