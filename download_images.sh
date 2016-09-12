wget -q http://vis-www.cs.umass.edu/lfw/lfw.tgz -O lfw.tgz
mkdir -p images
tar -xvf lfw.tgz -C images/
rm -fr lfw.tgz
mkdir -p data
mkdir -p db

