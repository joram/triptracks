sudo -u postgres dropdb tplanner
sudo su - postgres -c 'createdb -T template_postgis -O tplanner tplanner'