all: basca stepminer kmeans shmulevich stats parallelizedGenes

basca: ./threshold_methods/basca.c
	gcc-15 -fopenmp -O3 -fPIC -shared -o ./threshold_methods/basca.so ./threshold_methods/basca.c

stepminer: ./threshold_methods/stepminer.c
	gcc-15 -fopenmp -O3 -fPIC -shared -o ./threshold_methods/stepminer.so ./threshold_methods/stepminer.c

kmeans: ./threshold_methods/kmeans.c
	gcc-15 -fopenmp -O3 -fPIC -shared -o ./threshold_methods/kmeans.so ./threshold_methods/kmeans.c

shmulevich: ./threshold_methods/shmulevich.c
	gcc-15 -fopenmp -O3 -fPIC -shared -o ./threshold_methods/shmulevich.so ./threshold_methods/shmulevich.c

stats: ./statistics_methods/statistics.c

	gcc-15 -O3 -fPIC -shared -o ./statistics_methods/statistics.so ./statistics_methods/statistics.c

parallelizedGenes: ./threshold_methods/methods_parallelized_genes.c

	gcc-15 -fopenmp -O3 -fPIC -shared -o ./threshold_methods/methods_parallelized_genes.so ./threshold_methods/methods_parallelized_genes.c

clear:
	rm ./threshold_methods/basca.so
	rm ./threshold_methods/stepminer.so
	rm ./threshold_methods/kmeans.so
	rm ./threshold_methods/shmulevich.so
	rm ./statistics_methods/statistics.so
	rm ./threshold_methods/methods_parallelized_genes.so

run: all
	python app.py