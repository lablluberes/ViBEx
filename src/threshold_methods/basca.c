#include <stdio.h>
#include <math.h>
#include <omp.h>
#include <stdlib.h>
#include <string.h>

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

    omp_set_num_threads(omp_get_max_threads());
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
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size - 1; j++) {
            cost_matrix[i][j] = 0.0;
        }
    }

    // initialize index matrix
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - 2; j++) {
            index_matrix[i][j] = 0;
        }
    }

    // initialize p matrix
    #pragma omp parallel for collapse(2)
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
    #pragma omp parallel for private(threadid)
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
                #pragma omp parallel for private(threadid, min_value, min_index, curr_value, i, d)
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
    #pragma omp parallel for private(threadid, z, i)
    
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
    #pragma omp parallel for private(threadid, h, z_, e, q_score, max_value, max_index, i, k)
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

/*
int main(){

    double gene[5] = {1772.47, 2108.5, 3205.1, 1133.63, 185.885};

    double data[97] = {0.7566794133, 0.7455017481385997, 0.7355852386575561, 0.7268633690762257, 0.7192696236139648, 0.71273748649013, 0.7072004419240775, 0.7025919741351639, 0.6988455673427455, 0.6958947057661788, 0.6936728736248203, 0.6921135551380263, 0.6911502345251533, 0.6907163960055579, 0.6907455237985961, 0.6911711021236248, 0.6919266152, 0.6929455472470784, 0.6941613824842163, 0.6955076051307701, 0.6969176994060966, 0.6983251495295517, 0.699663439720492, 0.7008660541982743, 0.7018664771822544, 0.7025981928917893, 0.702994685546235, 0.7029894393649482, 0.7025159385672852, 0.7015076673726024, 0.6998981100002564, 0.6976207506696035, 0.6946090736, 0.6908286995316317, 0.6863737952880005, 0.6813706642134375, 0.675945609652274, 0.670224934948841, 0.6643349434474697, 0.6584019384924912, 0.6525522234282367, 0.6469121015990372, 0.6416078763492241, 0.6367658510231282, 0.6325123289650809, 0.6289736135194134, 0.6262760080304565, 0.6245458158425417, 0.6239093403, 0.6244522305796908, 0.6260975191885864, 0.6287275844661876, 0.6322248047519949, 0.6364715583855092, 0.6413502237062308, 0.6467431790536606, 0.6525328027672991, 0.6586014731866471, 0.6648315686512051, 0.6711054675004736, 0.6773055480739536, 0.6833141887111458, 0.6890137677515503, 0.6942866635346683, 0.6990152544, 0.7031079984245564, 0.7065776726353881, 0.7094631337970562, 0.7118032386741211, 0.7136368440311439, 0.7150028066326851, 0.715939983243306, 0.7164872306275669, 0.716683405550029, 0.7165673647752528, 0.7161779650677993, 0.7155540631922294, 0.7147345159131037, 0.7137581799949829, 0.7126639122024281, 0.7114905693, 0.7102770080522594, 0.7090620852237671, 0.7078846575790839, 0.7067835818827707, 0.7057977148993881, 0.7049659133934971, 0.7043270341296585, 0.703919933872433, 0.7037834693863816, 0.7039564974360648, 0.7044778747860435, 0.7053864582008789, 0.7067211044451314, 0.7085206702833619, 0.7108240124801312, 0.7136699878};

    double data2[5] = {1772.47, 1772.47, 1772.47, 1772.47, 0};

    double thr;

    double thr2 = BASCA(data, 97, 1);

    // se supone que sea kmeans {0: 0.6737218344374016}
    for(int i = 0; i < 10; i++){

        for(int j = 0; j < 100; j++){

            thr = BASCA(data, 97, i+1);

            printf(" thr: %.20lf threads numbers: %d iter: %d\n\n", thr, i+1, j+1);


            if(thr != thr2){
                printf("NOT SAME\n");
                break;
            }
        }
        if(thr != thr2){
                printf("NOT SAME\n");
                break;
            }

    }

}*/