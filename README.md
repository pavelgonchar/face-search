# face-search
Face search engine

Download demo dataset (Gary B. Huang, Manu Ramesh, Tamara Berg, and Erik Learned-Miller.
Labeled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments.
University of Massachusetts, Amherst, Technical Report 07-49, October, 2007.) or/and add your own images

```
./download_images.sh
```

Generate db:
```
cd code
./create_db.sh
```

Search by face:
```
# csv output
./run.sh URL 0
# image output
./run.sh URL 1
```
Query:
-----
![mr_bean](code/mr_bean.jpg?raw=true "mr_bean.jpg")
Results:
-------
![result](code/result.jpg?raw=true "result.jpg")

requirements:
```
sudo apt-get install imagemagick
sudo pip install awscli
sudo pip install click
```
