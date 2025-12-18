all: basca stepminer kmeans shmulevich

basca: ./basca.c
	gcc-15 -fopenmp -O3 -fPIC -shared -o ./basca.so ./basca.c

stepminer: ./stepminer.c
	gcc-15 -fopenmp -O3 -fPIC -shared -o ./stepminer.so ./stepminer.c

kmeans: ./kmeans.c
	gcc-15 -fopenmp -O3 -fPIC -shared -o ./kmeans.so ./kmeans.c

shmulevich: ./shmulevich.c
	gcc-15 -fopenmp -O3 -fPIC -shared -o ./shmulevich.so ./shmulevich.c

clear:
	rm ./basca.so
	rm ./stepminer.so
	rm ./kmeans.so
	rm ./shmulevich.so

run: all
	python app.py