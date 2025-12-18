import numpy as np
import ctypes

# gcc-15 -O3 -fPIC -shared -o main.so main.c -fopenmp

if __name__ == "__main__":
    
    np.random.seed(42)
        
    #print(matrix)
    
    run_lib = ctypes.CDLL('main.so')

    # Define the argument and return types for the functions
    run_lib.run.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'), ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
    run_lib.run.restype = None
    
    run_lib.modifyN.argtypes = [ctypes.c_int]
    run_lib.modifyN.restype = None
    
    run_lib.modifyM.argtypes = [ctypes.c_int]
    run_lib.modifyM.restype = None
    
    #NList = [10, 12, 14]
    #MList = [200, 400, 600]
    
    NList = [100, 200]
    MList = [100, 200]
    
    for N, M in zip(NList, MList):
    
        matrix = np.random.rand(N, M)
        
        for i in range(len(matrix)):
            matrix[i] = sorted(matrix[i])
        
        run_lib.modifyN(N)
        run_lib.modifyM(M)
        
        print(matrix)
        
        #ax = matrix.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        
        # compute thr using c code 
        run_lib.run(matrix, N, M, f"performance_{N}x{M}.csv".encode('utf-8'))