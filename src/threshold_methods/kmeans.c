 /******************************************************************************/
    /*										  *
     *   Purpose:     This code implements OpenMP in the k-means algorithm.
                      The main function reads a txt file with each row being a gene
                      expression. It then sends each row to the kmeans function where
                      the algorithm is implemented using OpenMP. To modify the file to be read
                      change the #define FILENAME line 
     *   Compile:     gcc-13 -fopenmp KMeans.c -o kmeans	  *
     *   Run:         ./kmeans
     *   Author:      Michael H. Terrefortes Rosado							  *
     *   Course:      CCOM6189 HPC						  *
     *   Last update: December 11, 2023	
     *   
     ******************************************************************************/
    

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#include <string.h>


// K-Means function where the method is implemented
// The function takes a vector as an argument
double KMeans(double vect[], const int size) {

    omp_set_num_threads(1);

    //printf("%d, %d", rand(), rand());

    // Initialize the centroids
    double centroidsUpdate[2] = {vect[0], vect[1]};

    // Initialize the past centroids to zero
    double centroidsPrev[2] = {0,0};

    //printf("Initial centroids: %f, %f\n", centroidsUpdate[0], centroidsUpdate[1]);
    //int maxIteration = 0;

    // eucledian distance of both centroids
    double distanceOne;
    double distanceTwo;

    // sum for the new mean of the centroids
    double sumCenOne;
    double sumCenTwo;
    int countOne;
    int countTwo;

    // binary array to flag each gene expression to cluster 1 or 2. 
    int binary[size];
    int nt, threadid;
    int chunks;

    int itr = 0;

                //double time = omp_get_wtime();

                //printf("calculating row\n");

    // while loop to keep assigning the genes until the centroid do not change or the maximum iteration is reached
    while(((centroidsUpdate[0] != centroidsPrev[0]) || (centroidsUpdate[1] != centroidsPrev[1])) && itr < 1000){

        // increase iteration
        itr++;

        // update the past centroids
        centroidsPrev[0] = centroidsUpdate[0];
        centroidsPrev[1] = centroidsUpdate[1];

                //printf("The centroids are %f, %f\n", centroidsUpdate[0], centroidsUpdate[1]);

        // start the first loop parallelization. the private variables are distanceOne, distanceTwo and threadid.
        #pragma omp parallel private(threadid, distanceOne, distanceTwo)
        {
            // get number of threads
            nt = omp_get_num_threads();
                     //printf("Number threads: %d\n", nt);

            // get the threadid
            threadid = omp_get_thread_num();
            //printf("Thread: %d \n", threadid);

            // get the chunk size so that the array is divided by the threads.
            chunks = size/nt;
            //printf("Thread: %d Chunks: %d\n itr: %d", threadid, chunks, itr);

            // parallelize for loop with schedule based on the chunks
            #pragma omp for schedule(static, chunks) 

                //printf("Chunks: %d thread: %d\n", chunks, threadid);

                for(int i = 0; i < size; i++){
                    // get the distance of the current gene to each centroid
                    distanceOne = centroidsUpdate[0] - vect[i];
                    distanceTwo = centroidsUpdate[1] - vect[i];

                    // if the distance is negative then multiply by one
                    // this is absolute value
                    if(distanceOne < 0){
                        distanceOne *= -1;
                    }
                    if(distanceTwo < 0){
                        distanceTwo *= -1;
                    }

                    // if the centroid one distance is less than the second then assign the gene
                    // to centroid 1
                    if(distanceOne < distanceTwo){
                        binary[i] = 1;
                    }

                    // assign the gene to centroid 2. 
                    else{
                        binary[i] = 2;
                    }

                }
        }

        // initialize variables
        sumCenOne = 0;
        sumCenTwo = 0;
        countOne = 0;
        countTwo = 0;

        // parallelize for loop using reduction. The operation is sum (+) and the variables are
        // sumcenone, sumcentwo, countone, countwo. 
        #pragma omp parallel for reduction(+: sumCenOne, sumCenTwo, countOne, countTwo) shared(binary)
        
        for(int j = 0; j < size; j++){

            // if the flag assigment of the gene is cluster one then 
            // sum that gene to the sumCenOne variable
            if(binary[j] == 1){
                sumCenOne += vect[j];
                countOne += 1;
            }

             // if the flag assigment of the gene is cluster two then 
            // sum that gene to the sumCenTwo variable
            else{
                sumCenTwo += vect[j];
                countTwo += 1;
            }
        }

        
        // update the centroids by getting a new mean
        centroidsUpdate[0] = sumCenOne / countOne;
        centroidsUpdate[1] = sumCenTwo / countTwo;

                        //printf("Updated centroids: %f, %f\n", centroidsUpdate[0], centroidsUpdate[1]);

                        //printf("iter %d\n", itr);

    }

                    //printf("returning threshold\n");

    // if the first centroid is nan then return the second centroid
    if(isnan(centroidsUpdate[0])){
        centroidsUpdate[0] = 0;
        return centroidsUpdate[1];
    }

    // if the second centroid is nan then return the first centroid
    if(isnan(centroidsUpdate[1])){
        centroidsUpdate[1] = 0;
        return centroidsUpdate[0];
    }

    // return the mean (which is the threshold) by adding both centroids and dividing by two.
    return (centroidsUpdate[0]+centroidsUpdate[1])/2;



}

/*
// Main function
int main() {

    //double data[9] = { 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};

    // thr es 2584.558333

    //double data[5] = {2080.5, 2404.2, 2526.5, 2798.4, 2865.7};

    double data[50] = {0,
 68.645,
 71.67,
 88.53666667,
 89.63666667,
 89.80833333,
 91.635,
 94.6,
 101.6083333,
 102.4816667,
 103.38,
 112.975,
 117.5366667,
 121.2633333,
 123.6283333,
 125.5916667,
 131.76,
 133.7833333,
 141.8766667,
 159.155,
 163.6133333,
 164.42,
 164.885,
 165.0283333,
 169.57,
 169.635,
 182.38,
 182.615,
 183.9533333,
 188.3966667,
 210.1783333,
 216.045,
 227.6633333,
 238.9266667,
 257.7633333,
 287.015,
 292.9166667,
 337.565,
 368.7466667,
 382.2266667,
 439.2416667,
 494.62,
 655.355,
 738.5883333,
 849.2483333,
 1190.89,
 1619.07,
 1726.663333,
 1921.125,
 2161.133333};

    int N = sizeof(data) / sizeof(data[0]);

    printf("Size of array before call: %d\n", N);
    
    double thr = KMeans(data, N);

    printf("Thr: %f\n", thr);

    return 0;
 

}
*/