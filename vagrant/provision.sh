sudo apt-get update 2> /dev/null

# Install essential packages
sudo apt-get -y install mc vim git ntpdate 2> /dev/null
sudo apt-get -y install python3-dev 2> /dev/null
sudo apt-get -y install virtualenv 2> /dev/null
sudo apt-get -y install build-essential libbz2-dev libfreetype6-dev libgdbm-dev 2> /dev/null
sudo apt-get -y install libjpeg-dev libltdl-dev 2> /dev/null
sudo apt-get -y install libreadline-dev libsasl2-dev libsqlite3-dev 2> /dev/null
sudo apt-get -y install libssl-dev libxslt1-dev ncurses-dev zlib1g-dev 2> /dev/null
sudo apt-get -y install make libldap2-dev libsasl2-dev libssl-dev libfontconfig 2> /dev/null
sudo apt-get -y install docker.io docker-compose 2> /dev/null
sudo apt-get -y remove ftp

# Configure date
echo 'TZ='Europe/Warsaw'; export TZ' > ~/.profile
sudo ntpdate-debian
sudo usermod -aG docker vagrant
mkdir /tmp/test-ftpdserver-pyconfr
mkdir /tmp/test-minio/

# Install application environment
if [ `grep 'activate' ~/.profile | wc -l` = 0 ]; then
virtualenv --python=python3.6 /home/vagrant/
echo "source bin/activate; cd project" >> ~/.profile
fi
source /home/vagrant/bin/activate
cd /home/vagrant/project/
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
pip install -r requirements/test.txt
pip install tox
pip install -e .

cd tests
sudo docker-compose pull
