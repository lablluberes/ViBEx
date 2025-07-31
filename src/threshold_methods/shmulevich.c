#include <stdio.h>
#include <math.h>
//#include <omp.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

int min(int m [], int index){

    int bestEle = m[0];
    int bestIndex = 0;

    for(int i = 0; i < index; i++){
        if(m[i] < bestEle){
            bestEle = m[i];
            bestIndex = i;
        }
    }

    return bestIndex;

}

double shmulevich(double data [], int const k){

    double D[k-1];

    for(int j = 0; j < k-1; j++){
        D[j] = data[j+1] - data[j];
    }

    double t = (data[k-1]-data[0]) / (k-1);

    int m[k]; 
    int index = 0;

    for(int j = 0; j < k-1; j++){
        if(D[j] > t){
            m[index] = j;
            index++;
        }
    }
       
    int m_index= min(m, index);

    return data[m_index+1];


}

/*
int main(){

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
    
    double thr = shmulevich(data, N);

    printf("Thr: %f\n", thr);

    return 0;
}*/