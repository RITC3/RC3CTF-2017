CC=gcc

all: debbie

deb-req.so: deb-req.c
	$(CC) -shared -o deb-req.so -fPIC deb-req.c

debbie.c: debbie.c.head debbie.c.tail
	cat debbie.c.head > debbie.c
	python make_debbie.py >> debbie.c
	cat debbie.c.tail >> debbie.c

debbie: deb-req.so debbie.c
	$(CC) -o debbie -O0 debbie.c deb-req.so

clean:
	rm -rf debbie.c debbie
