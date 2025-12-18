#include <stdio.h>
#include <math.h>
#include <omp.h>
#include <stdlib.h>
#include <string.h>

// to run:      gcc-15 main.c basca.c kmeans.c shmulevich.c stepminer.c -o my_program -fopenmp -O3


// This is the mean function from a to b
double Y_a_b(double vect[], int a, int b){

    double sum = 0;

    // if i want the mean from a==b then return the sigle number in a
    if(a == b){
        return vect[a];
    }

    //#pragma omp parallel for reduction(+: sum) 

    // sum the numbers from a to b-1
    for(int i = a; i < b; i++){
        sum += vect[i];
    }

    // return the mean
    return (sum / (b - a));

}

// Function to calculate the cost of the discontinuity
double C_a_b(double vect[], int a, int b){

    // get the mean from a to b
    double mean = Y_a_b(vect, a, b);

    double sum = 0;

    // if a==b then the cost is this
    if(a == b){
        return pow(vect[a] - mean, 2);
    }

    //#pragma omp parallel for reduction(+: sum) 

    // sum the cost based on this formula
    for(int i = a; i < b; i++){
        sum += pow(vect[i] - mean, 2);
    }

    // return cost
    return sum;

}

// partition function for quicksort
// arguments are the array, left anf right indexes
int partition(double arr[], int l, int r){
    // pivot variable
    double pivot = arr[r];
    int i = l - 1;

    // for loop to rearrange numbers
    for(int j = l; j < r; j++){
        if(arr[j] <= pivot){
            i++;
            double temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    // last rearragne
    double temp = arr[i + 1];
    arr[i + 1] = arr[r];
    arr[r] = temp;

    // return i
    return i + 1;
}


// quicksort algorithm to sort array
// parameters are array, left and right index
void quicksort(double arr[], int l, int r){
    // if left is less than right
    if(l < r){
        // call partition function and save result to pivot
        int pivot = partition(arr, l, r);
        // call quicksort
        quicksort(arr, l, pivot - 1);
        quicksort(arr, pivot + 1, r);
    }
}

// function to calculate the median of the array
double Find_median(double array[] , int n)
{
    double median=0;
    
    // if number of elements are even
    if(n%2 == 0)
        median = (array[(n-1)/2] + array[n/2])/2.0;
    // if number of elements are odd
    else
        median = array[n/2];
    
    return median;
}


// Function whith the BASCA algorithm 
double BASCA (double vect[], const int size) {

    //omp_set_num_threads(threadN);
    //omp_set_num_threads(threads);
    //double time = omp_get_wtime();

    // sort one of the vectors
    //quicksort(vect, 0, size-1);

                //const int size = sizeof(vect) / sizeof(vect[0]);

    // Initialize variables and matrixes
    double min_value, curr_value;
    int min_index;
    
    //double cost_matrix[size][size-1];
    //int index_matrix[size-1][size-2];
    //int P[size-2][size-2];

    // Allocating memory instead of declaring size because of segmentation fault when using big matrixes
    // https://stackoverflow.com/questions/1847789/segmentation-fault-on-large-array-sizes
    // https://www.geeksforgeeks.org/dynamically-allocate-2d-array-c/
    // https://labex.io/tutorials/c-how-to-manage-large-matrix-in-c-435499

    double **cost_matrix = malloc(size * sizeof(double *));
    for (int i = 0; i < size; i++) {
        cost_matrix[i] = malloc((size - 1) * sizeof(double));
    }

    int **index_matrix = malloc((size - 1) * sizeof(int *));
    for (int i = 0; i < size - 1; i++) {
        index_matrix[i] = malloc((size - 2) * sizeof(int));
    }

    // Allocate P[size-2][size-2]
    int **P = malloc((size - 2) * sizeof(int *));
    for (int i = 0; i < size - 2; i++) {
        P[i] = malloc((size - 2) * sizeof(int));
    }

    // initialize cost matrix
    //#pragma omp parallel for collapse(2)
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size - 1; j++) {
            cost_matrix[i][j] = 0.0;
        }
    }

    // initialize index matrix
    //#pragma omp parallel for collapse(2)
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - 2; j++) {
            index_matrix[i][j] = 0;
        }
    }

    // initialize p matrix
    //#pragma omp parallel for collapse(2)
    for (int i = 0; i < size - 2; i++) {
        for (int j = 0; j < size - 2; j++) {
            P[i][j] = 0;
        }
    }

    // Step 1: Compute a Series of Step Function

    // initialization C_i_(0) = c_i_N
    // calculate first cost matrix column with no intermidiate break points

    int threadid, nt; 
    int chunks;
    //double time = omp_get_wtime();

    // parallelize the first step
    //#pragma omp parallel for private(threadid)
    for (int i = 0; i < size; i++){
                             //printf("Thread %d put value %f in Array space [%d][%d]\n", threadid, C_a_b(vect, i, size), i, 0);
                cost_matrix[i][0] = C_a_b(vect, i, size);
            }


    int i, d;
    double var;
    double cost;
    
    // Algorithm 1: Calculate optimal step functions

    // Palrallelize the calculation optimal step functions algorithm
    for(int j = 0; j < size-2; j++){
            // in each column parallelize so that each thread can calculate a chunk of the cost
                //#pragma omp parallel for private(threadid, min_value, min_index, curr_value, i, d)
                for(int i = 0; i < size-j-1; i++){

                    // find the min_value and index of the minimum cost of
                    // additional intermediate break points
                    min_value = INFINITY;
                    min_index = -1;

                    for(int d = i; d < size-j-1; d++){

                        curr_value = C_a_b(vect, i, d+1) + cost_matrix[d+1][j];

                        if(curr_value < min_value){
                            min_value = curr_value;
                            min_index = d;
                            var = C_a_b(vect, i, d+1);
                            cost = cost_matrix[d+1][j];
                        }
                    }
                            //printf("Thread %d put value %f in Array space [%d][%d] this thread went from %d to %d %f, %f\n", threadid, min_value, i, j+1, j, chunks, var, cost);

                    // save the minimum value and index to cost and index matrix
                    cost_matrix[i][j+1] = min_value;
                    index_matrix[i][j] = min_index+1;

                }
            }


                    /*for(int i = 0; i < size; i++){
                        for(int j = 0; j < size-1; j++){
                            printf("%f ", cost_matrix[i][j]);
                        }
                        printf("\n");
                    }

                    printf("\n");
                    for(int i = 0; i < size-1; i++){
                        for(int j = 0; j < size-2; j++){
                            printf("%d ", index_matrix[i][j]);
                        }
                        printf("\n");
                    }*/

    //  Algorithm 2: Compute the break points of all optimal step functions

    int z;

    // Parallelize the second algorithm which is the P matrix calculation
    //#pragma omp parallel for private(threadid, z, i)
    
    for(int j = 0; j < size-2; j++){
                z = j;
                            //printf("Thread %d saved %d in [%d][%d]\n", threadid, index_matrix[0][z], i, j);
                // initialize first column
                P[0][j] = index_matrix[0][z];

                if(j > 0){
                    z = z - 1;

                    for(i = 1; i <= j; i++){
                        //printf("Thread %d saved %d in [%d][%d]\n", threadid,  index_matrix[P[i-1][j]][z], i, j);

                        // save the index of the optimal step function
                        P[i][j] = index_matrix[P[i-1][j]][z];
                        z = z - 1;
                    }
                }
            }

                        /*printf("\n");
                        for(int i = 0; i < size-2; i++){
                            for(int j = 0; j < size-2; j++){
                                printf("%d ", P[i][j]);
                            }
                            printf("\n");
                        }*/

    // Step 2: Find Strongest Discontinuity in Each Step Function

    double v[size-2];

    // initialize the v vector
    for(int i = 0; i < size-2; i++){
        v[i] = 0.0;
    }

    double max_value, h, z_, e, q_score;
    int max_index;
    int N = size;
    int k;

    // paralleize the algorithm to search for the strongest discontinuity
    //#pragma omp parallel for private(threadid, h, z_, e, q_score, max_value, max_index, i, k)
    for(int j = 0; j < size-2; j++){
                max_value = -INFINITY;
                max_index = -1;

                // calculate the maximum jump based on height, error, and qscore. 
                for(i = 0; i <= j; i++){

                    if(i == 0 && j == 0)
                    {
                        h = Y_a_b(vect, P[i][j], size) - Y_a_b(vect, 0, P[i][j]);
                    }
                    else if(i == 0 && j > 0)
                    {
                        h = Y_a_b(vect, P[i][j], P[i+1][j]) - Y_a_b(vect, 0, P[i][j]);
                    }
                    else if(i == j && i > 0)
                    {
                        h = Y_a_b(vect, P[i][j], size) - Y_a_b(vect, P[i-1][j], P[i][j]);
                    }
                    else
                    {
                        h = Y_a_b(vect, P[i][j], P[i+1][j]) - Y_a_b(vect, P[i-1][j], P[i][j]);
                    }

                    z_ = (vect[P[i][j]-1] + vect[P[i][j]]) / 2;

                    e = 0;

                    for(k = 0; k < size; k++){

                        e += pow(vect[k] - z_, 2);
                    }

                    q_score = h / e;
                    
                    // save the maximum height jump
                    if(q_score > max_value){
                        //printf("h: %f, e: %f, z: %f, qscore: %f, i: %d, j: %d\n", h, e, z_, q_score, i, j);
                        max_value = q_score;
                        max_index = i;
                    }

                }
                            //printf("Thread %d saves %d in space %d of v\n", threadid, P[max_index][j], j);

                // save the strongest discontinuity in the vector. 
                v[j] = P[max_index][j];

            }

                        /*for(int i = 0; i < size-2; i++){
                            printf("%d ", v[i]);
                        }*/

    // Step 3: Estimate Location and Variation of the Strongest Discontinuities

    // sort the v vector
    quicksort(v, 0, size-3);

    // find the median of the vector v
    int v_median = round(Find_median(v, size-2));

    // calculate the threshold that will be used to binarize 
    double thr = (vect[v_median-1] + vect[v_median]) / 2;

    //double elapsedTime = omp_get_wtime() - time;

    // print time
    //printf("\nElapsed time: %f\n", elapsedTime);

    for (int i = 0; i < size; i++)
        free(cost_matrix[i]);


    for (int i = 0; i < size - 1; i++) {
        free(index_matrix[i]);
    }

    for (int i = 0; i < size - 2; i++) {
        free(P[i]);
    }

    free(cost_matrix);
    free(index_matrix);
    free(P);

    return thr;


}


// K-Means function where the method is implemented
// The function takes a vector as an argument
double KMeans(double G[], const int size){

    srand(42);

    //omp_set_num_threads(threadN);

    //printf("\nk-means\n");

    double cn_j[2], co_j[2];

    int index1 = rand()%size;
    //int index2 = rand()%size;

    //printf("%d, %d ", index1, index2);

    cn_j[0] = G[index1];

    int index2;
    do{
        index2 = rand()%size;
        cn_j[1] = G[index2];
    }while (cn_j[0] == cn_j[1]);
    
    //printf("%d, %d ", index1, index2);
    
    co_j[0] = -1;
    co_j[1] = -1;

    int S[size];
    int iter = 0;

    double sum1;
    double sum2;
    int count1;
    int count2;

    double dis_1, dis_2;

    //printf("centroids init %f, %f\n", cn_j[0], cn_j[1]);

    while((cn_j[0] != co_j[0] || cn_j[1] != co_j[1]) && iter < 1000){
        
        co_j[0] = cn_j[0];
        co_j[1] = cn_j[1];

        //printf("prev centroids: %f, %f\n", co_j[0], co_j[1]);

        iter += 1;

        sum1 = 0;
        sum2 = 0;
        count1 = 0;
        count2 = 0;

        //#pragma omp parallel for shared(S, sum1, count1, count2, sum2, co_j) private(dis_1, dis_2)
        for(int i = 0; i < size; i++){
            //printf("index %d\n", i);
            dis_1 = fabs(G[i] - co_j[0]) * fabs(G[i] - co_j[0]);
            dis_2 = fabs(G[i] - co_j[1]) * fabs(G[i] - co_j[1]);
            
            //#pragma omp critial
            if(dis_1 < dis_2){
                S[i] = 1;
                //sum1 += G[i];
                //count1 += 1;
            }
            else{
                S[i] = 2;
                //sum2 += G[i];
                //count2 += 1;
            }
        }

        //#pragma omp parallel for reduction(+:sum1, sum2, count1, count2)
        for(int i = 0; i < size; i++){

            if(S[i] == 1){
                sum1 += G[i];
                count1 += 1;
            }
            else{
                sum2 += G[i];
                count2 += 1;
            }
        }

        //printf("ya\n");
        if(count1 > 0){
      
            cn_j[0] = sum1 / count1;
        }

        if(count2 > 0){
        
            cn_j[1] = sum2 / count2;
        }

        //for(int i = 0; i < size; i++){
        //    printf("%d ", S[i]);
        //}
        //printf("\n");

        //printf("new centroids: %f, %f\n", cn_j[0], cn_j[1]);

    
    }

    //printf("iters: %d\n", iter);

    //printf("last centroids: %f, %f\n", cn_j[0], cn_j[1]);

    return (cn_j[0]+cn_j[1]) / 2;
}


int min(int m [], int index){

    int bestEle = m[0];
    int bestIndex = 0;

    //#pragma omp parallel for
    for(int i = 0; i < index; i++){
        if(m[i] < bestEle){
            bestEle = m[i];
            bestIndex = i;
        }
    }

    return bestEle;

}

double shmulevich(double data [], int const k){

    //omp_set_num_threads(threadN);

    double D[k-1];
    int d_size = 0;
    //int comienza;
    int index_D[k-1];

    //printf("aqui\n");

    //#pragma omp parallel for
    for(int j = 0; j <= k-2; j++){
        //printf("aaa");
        //printf("aqio");
        //if(((data[j+1] >= min_gene) && (data[j+1] <= max_gene)) && ((data[j] >= min_gene) && (data[j] <= max_gene))){
            //printf("aqio");
        D[j] = data[j+1] - data[j];

        index_D[j] = j;

            //printf("index: %d, %f, ",j,  D[d_size]);
        d_size++;
        //}
        //else{
        //    D[j] = -1.0;
        //    index_D[j] = -1;
        //}
    }

    //printf("aaa");

    double t = (data[k-1]-data[0]) / (k-1);
    //printf("\n t: %f\n", t);

    int m[k-1]; 
    int index = 0;

    //#pragma omp parallel for
    for(int j = 0; j <= k-2; j++){
       
        if(D[j] > t){
            m[index] = index_D[j];
            //printf(" j: %d, ", index_D[j]);
            index++;
        }
      
    }
       
    int m_index= min(m, index);

    //printf(" index: %d ", m_index);

    return data[m_index+1];


}


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

    
    //omp_set_num_threads(threadN);
    //omp_set_num_threads(thrs);
  

    //printf("%f\n", xmean);
    //printf("%f", SSTOT);

    double leftMean, rightMean, SSE, t;
    int nt, threadid, chunks;

    for(int i = 0; i < 1; i++){
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


        if(SSEmin > SSE){
            SSEmin = SSE;

            t = (leftMean + rightMean)/2;
            //printf("%f",t);

        }
    }

    //#pragma omp parallel for private(SSE, rightMean, leftMean) shared(SSEmin, t, x)
    

        //nt = omp_get_num_threads();
        //printf("Number threads: %d\n", nt);
        //threadid = omp_get_thread_num();
        //printf("Thread: %d\n", threadid);
        //chunks = N/nt;
        //printf("Chunks: %d\n", chunks);

        //#pragma omp for schedule(static, chunks)
    for(int i = 1; i < N-1; i++){
            //int thread_id = omp_get_thread_num();
            //int num_threads = omp_get_num_threads();
          
            //printf("Thread %d processing index %d\n", thread_id, i);

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
            
            //#pragma omp critical
            if(i == 0){
                SSEmin = SSE;
            }


            //printf("%f\n", SSE);
            //#pragma omp critical
            if(SSEmin > SSE){
                SSEmin = SSE;

                t = (leftMean + rightMean)/2;
                //printf("%f",t);

            }
        }


    //double elapsedTime = omp_get_wtime() - time;

    // print time
    //printf("\nElapsed time: %f\n", elapsedTime);

    //printf("stepminer %f\n",t);

    return t;
}


int N = 10;
int M = 10;

//double thrs[];


void modifyN(int totalG){
    N = totalG;
}

void modifyM(int sizeG){
    M = sizeG;
}

//double returnThrValues(int i){
//    return thrs[i];
//}

// gcc-15 -fopenmp -O3 -fPIC -shared -o ./methods.so ./methods.c

double* run(double matrix[N][M], int totalGenes, int sizeGenes, char method[]){

    double* thrs = (double*)malloc(totalGenes * sizeof(double));

    omp_set_num_threads(10);


    #pragma omp parallel for
    for(int i = 0; i < totalGenes; i++){
        if(strcmp(method, "basc") == 0){

            thrs[i] = BASCA(matrix[i], sizeGenes);
            //printf("thr: %f\n", BASCA(matrix[i], sizeGenes));
        }
        else if(strcmp(method, "kmeans") == 0){

            thrs[i] = KMeans(matrix[i], sizeGenes);
        }
        else if(strcmp(method, "onestep") == 0){

            thrs[i] = stepminer(matrix[i], sizeGenes);
        }
        else {

            //printf("thr: %f\n", shmulevich(matrix[i], sizeGenes));
            thrs[i] = shmulevich(matrix[i], sizeGenes);
        }
        
         
    }

    return thrs;

}