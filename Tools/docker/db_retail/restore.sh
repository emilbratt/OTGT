#!/usr/bin/env bash

# SET CORRECT VALUES FOR EACH BEFORE RUNNING
_CONTAINER=db_retail
_PASSWORD=Mys3cretPWD
_FILE_DB_BAK=$HOME/DB.bak

function restore_backup () {
  if ! [ -f $_FILE_DB_BAK ]; then
    echo "$_FILE_DB_BAK does not exist"
    return 1
  fi
  docker exec -it $_CONTAINER mkdir -p /var/opt/mssql/backup

  docker cp $_FILE_DB_BAK \
            $_CONTAINER:/var/opt/mssql/backup/DB.bak

  docker exec -it $_CONTAINER /opt/mssql-tools/bin/sqlcmd \
   -S localhost -U SA -P $_PASSWORD \
   -Q 'RESTORE DATABASE HIP FROM DISK = "/var/opt/mssql/backup/DB.bak" WITH MOVE "HIP" TO "/var/opt/mssql/data/HIP.mdf", MOVE "HIP_log" TO "/var/opt/mssql/data/HIP_log.ndf"'

}

function list_databass () {
  docker exec -it $_CONTAINER /opt/mssql-tools/bin/sqlcmd \
    -S localhost \
    -U SA -P "$_PASSWORD" \
    -Q 'RESTORE FILELISTONLY FROM DISK = "/var/opt/mssql/backup/DB.bak"' \
    | tr -s ' ' | cut -d ' ' -f 1-2
}

function open_sql_shell () {
  _cmd="/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P $_PASSWORD"
  docker exec -it $_CONTAINER $_cmd
}


clear
echo '--Restore Database--'
echo "File to restore from $_FILE_DB_BAK"
echo "Docker container name $_CONTAINER"
echo "User sa password $_PASSWORD"


echo "1 restore $_FILE_DB_BAK to MS SQL container (make sure file and container exists first)"
echo '2 list database files from backup inside '
echo '3 open sql shell inside container'
echo '0 exit'

printf 'Type number: '; read _OPTN

if [[ $_OPTN == 0 ]]; then
  exit
elif [[ $_OPTN == '1' ]]; then
  restore_backup
elif [[ $_OPTN == 2 ]]; then
  list_databass
elif [[ $_OPTN == 3 ]]; then
  open_sql_shell
fi
