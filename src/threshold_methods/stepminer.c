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

    
    omp_set_num_threads(omp_get_max_threads());
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

    #pragma omp parallel for private(SSE, rightMean, leftMean) shared(SSEmin, t, x)
    

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
            
            #pragma omp critical
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


    //double elapsedTime = omp_get_wtime() - time;

    // print time
    //printf("\nElapsed time: %f\n", elapsedTime);

    //printf("stepminer %f\n",t);

    return t;
}



/*

int main(){

    double gene[5] = {1772.47, 2108.5, 3205.1, 1133.63, 185.885};

    double data[97] = {0.7566794133, 0.7455017481385997, 0.7355852386575561, 0.7268633690762257, 0.7192696236139648, 0.71273748649013, 0.7072004419240775, 0.7025919741351639, 0.6988455673427455, 0.6958947057661788, 0.6936728736248203, 0.6921135551380263, 0.6911502345251533, 0.6907163960055579, 0.6907455237985961, 0.6911711021236248, 0.6919266152, 0.6929455472470784, 0.6941613824842163, 0.6955076051307701, 0.6969176994060966, 0.6983251495295517, 0.699663439720492, 0.7008660541982743, 0.7018664771822544, 0.7025981928917893, 0.702994685546235, 0.7029894393649482, 0.7025159385672852, 0.7015076673726024, 0.6998981100002564, 0.6976207506696035, 0.6946090736, 0.6908286995316317, 0.6863737952880005, 0.6813706642134375, 0.675945609652274, 0.670224934948841, 0.6643349434474697, 0.6584019384924912, 0.6525522234282367, 0.6469121015990372, 0.6416078763492241, 0.6367658510231282, 0.6325123289650809, 0.6289736135194134, 0.6262760080304565, 0.6245458158425417, 0.6239093403, 0.6244522305796908, 0.6260975191885864, 0.6287275844661876, 0.6322248047519949, 0.6364715583855092, 0.6413502237062308, 0.6467431790536606, 0.6525328027672991, 0.6586014731866471, 0.6648315686512051, 0.6711054675004736, 0.6773055480739536, 0.6833141887111458, 0.6890137677515503, 0.6942866635346683, 0.6990152544, 0.7031079984245564, 0.7065776726353881, 0.7094631337970562, 0.7118032386741211, 0.7136368440311439, 0.7150028066326851, 0.715939983243306, 0.7164872306275669, 0.716683405550029, 0.7165673647752528, 0.7161779650677993, 0.7155540631922294, 0.7147345159131037, 0.7137581799949829, 0.7126639122024281, 0.7114905693, 0.7102770080522594, 0.7090620852237671, 0.7078846575790839, 0.7067835818827707, 0.7057977148993881, 0.7049659133934971, 0.7043270341296585, 0.703919933872433, 0.7037834693863816, 0.7039564974360648, 0.7044778747860435, 0.7053864582008789, 0.7067211044451314, 0.7085206702833619, 0.7108240124801312, 0.7136699878};

    double data2[5] = {1772.47, 1772.47, 1772.47, 1772.47, 0};

    double thr;

    double thr2 = stepminer(data, 97, 1);

    // se supone que sea kmeans {0: 0.6737218344374016}
    for(int i = 0; i < 10; i++){

        for(int j = 0; j < 100; j++){

            thr = stepminer(data, 97, i+1);

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