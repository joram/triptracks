
# add repos for postgis and postgres
# deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main
# wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
# sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
# sudo apt-get update
# sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 postgis postgresql-server-dev-9.3 python-psycopg2
# sudo pip install psycopg2 python2.7-dev --upgrade


# # Allows non-superusers the ability to create from this template
#sudo su - postgres -c psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"

# create postgis template db
chmod 755 ./scripts/create_postgis-2.1.sh
sudo -u postgres dropdb template_postgis
sudo -u postgres ./scripts/create_postgis-2.1.sh

# create project db
sudo -u postgres dropdb tplanner
sudo -u postgres psql -c "CREATE USER tplanner WITH PASSWORD 'tplanner';"
sudo su - postgres -c 'createdb -T template_postgis -O tplanner tplanner'

# update django settings
# psql -U tplanner -h localhost tplanner
# select postgis_lib_version();
# add POSTGIS_VERSION = (1, 5, 8) to django settings

sudo service postgresql restart