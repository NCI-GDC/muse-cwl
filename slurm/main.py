import postgres
import argparse

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="MuSE variant calling pipeline")

    required = parser.add_argument_group("Required input parameters")
    required.add_argument("--host", default='pgreadwrite.osdc.io', help='hostname for db')
    required.add_argument("--database", default='prod_bioinfo', help='name of the database')
    required.add_argument("--username", default=None, help="username for db access", required=True)
    required.add_argument("--password", default=None, help="password for db access", required=True)

    args = parser.parse_args()

    DATABASE = {
        'drivername': 'postgres',
        'host' : args.host,
        'port' : '5432',
        'username': args.username,
        'password' : args.password,
        'database' : args.database
    }
    
    engine = postgres.db_connect(DATABASE)
    (tumor, tumor_file, normal, normal_file) = postgres.get_complete_cases(engine)

    for case_id in tumor:
        for tum in tumor[case_id]:
            for norm in normal[case_id]:
                pair = [norm, tum]
                print case_id, pair
                postgres.add_status(engine, case_id, pair, "TBD", "unknown")
