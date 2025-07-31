#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

double my_string_p;
double highest_p = -1.0;
char *highest_string;

void readFile(double *prob_alg, double *prob_val, int rangeIndex, int alg){

    char name[100];

    snprintf(name, 100, "./statistics_methods/cdf_%d.csv", rangeIndex+1);

    FILE *file = fopen(name, "r");

    char line[1024];
    
    if (fgets(line, sizeof(line), file) == NULL) {
        fclose(file); 
    }

    int index = 0;

    while (fgets(line, sizeof(line), file) != NULL) {
   
        line[strcspn(line, "\n")] = 0;

        char *token;
        token = strtok(line, ",");
   
        int count = 0;
        while (token != NULL) {

            if (count == alg){
                prob_alg[index] = atof(token);
            }

            if (count == 4){
                prob_val[index] = atof(token);
            }
            count ++;

            token = strtok(NULL, ",");
        }

        index++; 
    
    }

    // Close the file
    fclose(file);

    return;
}

int bisect_right(double arr[], double x) {
    int low = 0;
    int high = 100; // Important: high is size, not size - 1
    int result = 100; // Default to inserting at the end if no suitable position found

    while (low < high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] > x) { // If mid element is strictly greater than x
            result = mid; // This could be our insertion point
            high = mid;   // Try to find an even earlier position
        } else {
            low = mid + 1; // Mid element is less than or equal to x, search in the right half
        }
    }
    return result;
}

int bisect_left(double arr[], double x) {
    int low = 0;
    int high = 100; // Important: high is size, not size - 1
    int result = 100; // Default to inserting at the end if no suitable position found

    while (low < high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] >= x) { // If mid element is greater than or equal to x
            result = mid; // This could be our insertion point
            high = mid;   // Try to find an even earlier position
        } else {
            low = mid + 1; // Mid element is less than x, search in the right half
        }
    }
    return result;
}

void prob(double vec[], double d, double probs_alg[], double probs_val[], int n1, int size, double prb[]){

    //printf("size: %d\n", n1);

    double *p = &vec[size];  

    double t = (vec[-n1+size]-d);

    int idx = bisect_right(probs_val, t);

    //printf("%f, %d", t, idx);

    if(idx < 1) idx = 0;
    if(idx > 99) idx = 99;

    double p1 = probs_alg[idx];

    t = (vec[-n1+size]+d);

    idx = bisect_left(probs_val, t);
    if(idx < 1) idx = 0;
    if(idx > 99) idx = 99;

    double p0 = 1 - probs_alg[idx];
    double pq = 1 - (p1 + p0);
    
    //double arr[3] = {p0, p1, pq};

    //return arr;

    //printf("al final de prob\n");

    prb[0] = p0;
    prb[1] = p1;
    prb[2] = pq;

    return;
    
}

void probPerm(double vec[], double d, int n, int n1, char x[], double p, double probs_alg[], double probs_val[], char my_string[]){

    if (n1 == 0){
        //if(strcmp(x, "1001010011110") == 0)
        //    printf("%s: %.9f\n",x, p);
        if(strcmp(x, my_string) == 0)
        {
            my_string_p = p;
        }
        if(p > highest_p){
            highest_p = p;
            highest_string = malloc(n * sizeof(char));
            strcpy(highest_string, x);
        }
        return;
    }

    else{

        double prb[3];

        //printf("get prob\n");

        prob(vec, d, probs_alg, probs_val, n1, n, prb);

        double p0, p1, pq;

        char x0[n + 1];
        strncpy(x0, x, n + 1);
        strncat(x0, "0", 1);

        p0 = p * prb[0];
        
        //printf("llamar recursiva\n");
        probPerm(vec, d, n, n1-1, x0, p0, probs_alg, probs_val, my_string);
    

        char x1[n + 1];
        strncpy(x1, x, n + 1);
        strncat(x1, "1", 1);

        p1 = p * prb[1];

        probPerm(vec, d, n, n1-1, x1, p1, probs_alg, probs_val, my_string);

        char xq[n + 1];
        strncpy(xq, x, n + 1);
        strncat(xq, "?", 1);
        
        pq = p * prb[2];

        probPerm(vec, d, n, n1-1, xq, pq, probs_alg, probs_val, my_string);

    }

}


void probBin(double gene[], double d, int sizeGene, double probs_alg[], double probs_val[], double min, char my_string[]){

    double res = floor(min*10)/10;

    for(int i = 0; i < sizeGene; i++){
        gene[i] = gene[i] - res;
        //printf("%f ", gene[i]);
    }

    char arr[5] = "";

    //printf("llamar permutation\n");

    clock_t start, end;
    double cpu_time_used;
     
    start = clock();

    probPerm(gene, d, sizeGene, sizeGene, arr, 1, probs_alg, probs_val, my_string);

    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    //printf("size %d aquiiii: %f\n", sizeGene, cpu_time_used); 

    return;

}

void run(double gene[], double d, int sizeGene, char alg[], char my_string[]){

    double min = gene[0], max = gene[0];
        for (int i = 1; i < sizeGene; i++) {
            if (gene[i] < min) min = gene[i];
            if (gene[i] > max) max = gene[i];
        }

    int rangeIndex = ceil((max-min)*10) - 1;

    double probs_alg[100], probs_val[100];

    //k-means,onestep,BASC_A,shmulevich,val
    int alg_number;
    
    if(strcmp(alg, "k-means") == 0)
    {
        alg_number = 0;
    }
    else if (strcmp(alg, "onestep") == 0)
    {
        alg_number = 1;
    }
    else if (strcmp(alg, "BASC_A") == 0)
    {
        alg_number = 2;
    }
    else
    {
        alg_number = 3;
    }
    
    //printf("%d \n\n", alg_number);

    readFile(probs_alg, probs_val, rangeIndex, alg_number);
    
    //for(int i = 0; i < 100; i++){
    //    printf("%f ", probs_alg[i]);
    //}

    probBin(gene, d, sizeGene, probs_alg, probs_val, min, my_string);

    return;

}

double get_high_p(){
    double p = highest_p;

    highest_p = -1.0;

    return p;
}

double get_p(){
    double p = my_string_p;
    my_string_p = 0;

    return p;
}

char *get_string(){

    size_t length = strlen(highest_string);

    //char arr[length];

    char *arr = malloc(length + 1);

    strcpy(arr, highest_string);

    free(highest_string);
    
    return arr;
}

/*
int main(){

    double gene[5] = {0.104088,  0.0456529, 0.0899751, 0.182464, 0.0397391};
    double d = 0.0032;
    char alg[10] = "k-means";
    int sizeGene = 5;

    run(gene, d, sizeGene, alg, "1?010");

    printf("highest string: %s, prob: %f my string p: %f\n", highest_string, highest_p, my_string_p);
    highest_p = 0;
    my_string_p = 0;
    free(highest_string);
    
    double gene1[10] = {0.104088,  0.0456529, 0.0899751, 0.182464,  0.0397391, 0.0932, 0.0851, 0.1019, 0.0894, 0.0970};
    run(gene1, d, 10, alg, "1??1000100");

    printf("highest string: %s, prob: %f my string p: %f\n", highest_string, highest_p, my_string_p);
    highest_p = 0;
    my_string_p = 0;
    free(highest_string);

    double gene2[13] = {0.104088  , 0.0456529 , 0.0899751 , 0.182464  , 0.0397391 ,   0.182464  , 0.07210751, 0.0397391 , 0.13845988, 0.13340002,   0.14899839, 0.09482894, 0.08228803};
    run(gene2, d, 13, alg, "10010100???00");

    printf("highest string: %s, prob: %f my string p: %f\n", highest_string, highest_p, my_string_p);
    highest_p = 0;
    my_string_p = 0;
    free(highest_string);

    double gene3[15] = {0.104088  , 0.0456529 , 0.0899751 , 0.182464  , 0.0397391 ,   0.182464  , 0.07210751, 0.0397391 , 0.13845988, 0.13340002,   0.14899839, 0.09482894, 0.08228803, 0.0397391 , 0.04502217};
    run(gene3, d, 15, alg, "10??01001110000");

    printf("highest string: %s, prob: %f my string p: %f\n", highest_string, highest_p, my_string_p);
    highest_p = 0;
    my_string_p = 0;
    free(highest_string);

    //double gene4[50] = {0.104088  , 0.0456529 , 0.0899751 , 0.182464  , 0.0397391 ,   0.182464  , 0.07210751, 0.0397391 , 0.13845988, 0.13340002,   0.14899839, 0.09482894, 0.08228803, 0.0397391 , 0.04502217,   0.182464  , 0.11878976, 0.04595516, 0.11877186, 0.14492543,   0.12920543, 0.10077983, 0.12206538, 0.05716041, 0.11400026,   0.10608877, 0.12505076, 0.1153136 , 0.06699311, 0.182464  ,   0.0397391 , 0.04965236, 0.06459848, 0.05807794, 0.07369502,   0.11049246, 0.09580436, 0.0397391 , 0.08706011, 0.12915618,   0.09906689, 0.0397391 , 0.08134486, 0.13013362, 0.182464  ,   0.05471957, 0.10810489, 0.0664399 , 0.0397391 , 0.14370657};
    //run(gene4, d, 50, alg);

    //printf("%s", file);

    //double prb[3];

    //prob(gene, d, probs_alg, probs_val, 1, 5, prb);

    return 0;
}*/