#include <stdio.h>
#include <math.h>
//#include <omp.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

double find_mean(double data [], int start, int end){

    if (start > end){
        return 0.0;
    }
        
    if(start == end) {
        return 0.0;
    }

    double result = 0.0;

    for(int i = start; i <= end; i++){
        result += data[i];
    }

    return result/(end-start+1);
}

double mse(double data [], int start, int end){

    double result = 0.0;

    double m = find_mean(data, start, end);

    for(int i = start; i <= end; i++){
        result += (data[i] - m) * (data[i] - m);

    }

    return result;

}

double sum(double data [], const int N){
    double result = 0.0;


    for(int i = 0; i < N; i++){
        result += data[i];
    }

    return result;
}


double stepminer(double data [], const int N){

    //const int N = sizeof(data) / sizeof(data[0]);

    //printf("Size: %d\n", N);

    //omp_set_num_threads(omp_get_max_threads());
    //omp_set_num_threads(5);

    double sseArray[N];
    double suma = sum(data, N);
    double mean = find_mean(data, 0, N-1);
    double sstot = mse(data, 0, N-1);
    double sum1 = 0;
    double count1 = 0;
    double m1 = 0;
    double sum2 = suma;
    double count2 = N;
    double m2 = (suma/N);
    double sum1sq = 0;
    double sum2sq = sstot;
    double sse = sum1sq + sum2sq;
    double entry = 0.0;
    double tmp = 0.0;

    //printf("aqui %f, %f, %f\n", suma, mean, sstot);

    
    for(int i = 0; i < N; i++){

            entry = data[i];

            count1 += 1;
            count2 -= 1;

            if(count2 == 0){
                sseArray[i] = sstot;
                continue;
            }

            tmp = (mean - (entry + sum1)/count1);
            sum1sq = sum1sq + (entry - mean) * (entry - mean) - tmp * tmp * count1 + (count1 - 1) * (mean - m1) * (mean - m1);
            tmp = (mean - (sum2 - entry)/count2);
            sum2sq = sum2sq - (entry - mean) * (entry - mean) - tmp * tmp * count2 + (count2 + 1) * (mean - m2) * (mean - m2);
            sum1 += entry;
            sum2 -= entry;
            m1 = sum1/count1;
            m2 = sum2/count2;
            sse = sum1sq + sum2sq;
            sseArray[i] = sse;

    }
    

    //for(int i = 0; i < N; i++){
    //    printf("%f, ", sseArray[i]);
    //}

    double bestSse = sseArray[0];
    int bestIndex = 0;
    int index = 0;

    for(int i = 0; i < N; i++){
        index = i;

        if(sseArray[i] < bestSse){
            bestSse = sseArray[i];
            bestIndex = index;
        }
    
    }

    //printf("%f, %d\n", bestSse, bestIndex);
    
    m1 = find_mean(data, 0, bestIndex);
    m2 = find_mean(data, bestIndex + 1, N-1);


    double thr = (m1+m2)/2;

    return thr;


}

/*
int main(){

    //double data[9] = { 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};

    // thr es 2584.558333

    double data[5] = {2080.5, 2404.2, 2526.5, 2798.4, 2865.7};

    int N = sizeof(data) / sizeof(data[0]);

    printf("Size of array before call: %d\n", N);
    
    thr = stepminer(data, N);

    printf("Thr: %f\n", thr);

    return 0;
}*/