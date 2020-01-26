from Setup.etl_db import etl



def main():
    # Create Argument Parser
    ap = argparse.ArgumentParser(description = "This script creates and loads the NYC Taxi dataset into a defined postgres db. For example, python etl_db.py --host=<server-name> --port=5432 --dbname=<database-name> --user=<admin-username> --password=<admin-password>")
    # Add the arguments to the parser
    ap.add_argument("-s", "--host", required=True, help="Enter <server-name>")
    ap.add_argument("-p", "--port", required=True, help="Enter <port-number>, default 5432")
    ap.add_argument("-d", "--dbname", required=True, help="Enter <database-name>, default postgres")
    ap.add_argument("-u", "--user", required=True, help="Enter <admin-username>")
    ap.add_argument("-a", "--password", required=True, help="Enter <admin-password>")
    ap.add_argument("-m", "--sslmode", required=True, help="ssl required or not - put either require/allow")
    args = vars(ap.parse_args())
    # Set db variables
    host = args['host']
    port = args['port']
    dbname = args['dbname']
    user = args['user']
    password = args['password']
    sslmode = args['sslmode']
    # pass info variables into etl pipeline to create db
    etl(host=host, port=port, dbname=dbname, user=user, password=password, sslmode=sslmode)


if __name__ == '__main__':
    # local insance - python create_db.py --host="localhost" --port=5432 --user="postgres" --dbname="postgres" --password="password" --sslmode="allow"
    # azure instance - python create_db.py --host="<server-name>" --port=5432 --user="<admin-username>" --dbname="<database-name>" --password="<admin-password>" --sslmode="require"
    main()

