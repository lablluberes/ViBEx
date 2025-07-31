#include <stdio.h>
#include <math.h>
#include <omp.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

double calcSSTOT(double x[], int n, double xmean){
    double m = 0;

    //#pragma omp parallel for reduction(+: m)
    for(int i = 0; i < n; i++){
        m = m + ( (x[i] - xmean) * (x[i] - xmean) );
    }
    

    return m;

}

double mean(double x[], int start, int end){
    double sum = 0;

    //#pragma omp parallel for reduction(+: sum)
    for(int i = start; i < end; i++){
        sum += x[i];
    }
    

    return sum/(end-start);
}

double stepminer(double x[], int N){

    //double time = omp_get_wtime();

    double xmean = mean(x, 0, N);

    double SSTOT = calcSSTOT(x, N, xmean);

    double SSEmin = 0;

    omp_set_num_threads(1);

    //printf("%f\n", xmean);
    //printf("%f", SSTOT);

    double leftMean, rightMean, SSE, t;
    int nt, threadid, chunks;

    #pragma omp parallel private(SSE, rightMean, leftMean) shared(SSEmin, t)
    {

        nt = omp_get_num_threads();
        //printf("Number threads: %d\n", nt);
        threadid = omp_get_thread_num();
        //printf("Thread: %d\n", threadid);
        chunks = N/nt;
        //printf("Chunks: %d\n", chunks);

        #pragma omp for schedule(static, chunks)
        for(int i = 0; i < N-1; i++){
            rightMean = mean(x, i+1, N);
            leftMean = mean(x, 0, i+1);

            //printf("%f\n", rightMean);
            //printf("%f\n", leftMean);

            SSE = 0;

            
            //#pragma omp parallel for reduction(+: SSE)

            for(int j = 0; j < N; j++){
                if(j < i+1){
                    SSE = SSE + ((x[j] - leftMean) * (x[j] - leftMean));

                }
                else {
                    SSE = SSE + ((x[j] - rightMean) * (x[j] - rightMean));
                }
            }

            if(i == 0){
                SSEmin = SSE;
            }


            //printf("%f\n", SSE);
            #pragma omp critical
            if(SSEmin > SSE){
                SSEmin = SSE;

                t = (leftMean + rightMean)/2;
                //printf("%f",t);

            }
        }
    }

    //double elapsedTime = omp_get_wtime() - time;

    // print time
    //printf("\nElapsed time: %f\n", elapsedTime);

    return t;
}