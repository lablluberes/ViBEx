all: basca stepminer onestep kmeans shmulevich stats

basca: ./threshold_methods/basca.c
	gcc-14 -fopenmp -O3 -fPIC -shared -o ./threshold_methods/basca.so ./threshold_methods/basca.c

stepminer: ./threshold_methods/stepminer.c
	gcc-14 -fopenmp -O3 -fPIC -shared -o ./threshold_methods/stepminer.so ./threshold_methods/stepminer.c

onestep: ./threshold_methods/onestep.c
	gcc-14 -O3 -fPIC -shared -o ./threshold_methods/onestep.so ./threshold_methods/onestep.c

kmeans: ./threshold_methods/kmeans.c
	gcc-14 -fopenmp -O3 -fPIC -shared -o ./threshold_methods/kmeans.so ./threshold_methods/kmeans.c

shmulevich: ./threshold_methods/shmulevich.c
	gcc-14 -O3 -fPIC -shared -o ./threshold_methods/shmulevich.so ./threshold_methods/shmulevich.c

stats: ./statistics_methods/statistics.c

	gcc-14 -O3 -fPIC -shared -o ./statistics_methods/statistics.so ./statistics_methods/statistics.c

clear:
	rm ./threshold_methods/basca.so
	rm ./threshold_methods/stepminer.so
	rm ./threshold_methods/onestep.so
	rm ./threshold_methods/kmeans.so
	rm ./threshold_methods/shmulevich.so
	rm ./statistics_methods/statistics.so

run: all
	python app.py