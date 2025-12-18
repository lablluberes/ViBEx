import numpy as np
from scipy.stats import gaussian_kde
import pandas as pd
from binarization.voting_algos import election_strings


def impute_all_string_with_threshold_probs(prob_matrix, ternary_vector, p_thresh):
  """
    Replace ternary string with highest prob string:
        - imputed_vector: 0/1/NA
        - imputed_probs: probability of the value for each position
    """
  ternary_vector = np.array(ternary_vector, dtype=object)
  n = len(ternary_vector)

  imputed_vector = []
  imputed_prob = []

  for prob in prob_matrix:
    # get maximum prob of time i
    m = max(prob)
    #print(m, prob)
    idx = list(prob).index(m)

    # append string
    if idx == 0:
      imputed_vector.append(0)
      imputed_prob.append(m)
    elif idx == 1:
      imputed_vector.append(1)
      imputed_prob.append(m)
    else:
      imputed_vector.append(np.nan)
      imputed_prob.append(m)

  #if np.prod(imputed_prob) < p_thresh:
  #  imputed_vector = ternary_vector.copy()

  return imputed_vector, imputed_prob


# --------------------------------------------------------------
# build KDE-based CDF from threshold samples
# --------------------------------------------------------------
def build_kde_cdf(threshold_samples, grid_n=2000, extend=0.1):
    """
    Fit a gaussian_kde to threshold_samples and return a CDF function cdf(t).
    - threshold_samples: 1D array of thresholds computed from random data
    - grid_n: number of grid points used to create CDF interpolation
    - extend: fraction to extend the grid range on both sides
    Returns: function cdf(t) that returns approximate CDF at t
    """
    samples = np.asarray(threshold_samples)
    if samples.size == 0:
        raise ValueError("threshold_samples must contain at least one value")

    kde = gaussian_kde(samples)
    # Build grid across a slightly extended range
    smin, smax = samples.min(), samples.max()
    span = smax - smin
    left = smin - max(1e-8, extend * span)
    right = smax + max(1e-8, extend * span)
    grid = np.linspace(left, right, grid_n)
    pdf_vals = kde(grid)
    # numeric cumulative integral
    dx = grid[1] - grid[0]
    cdf_vals = np.cumsum(pdf_vals) * dx
    # normalize to ensure last value is 1 (guard against tiny numeric issues)
    cdf_vals /= cdf_vals[-1]

    def cdf_func(x):
        # vectorized interp of x on grid -> cdf values
        return np.interp(x, grid, cdf_vals, left=0.0, right=1.0)

    return cdf_func

# -------------------------------
# 1: compute per-method probabilities (using threshold-PDF CDF)
# -------------------------------
def compute_probs_from_threshold_kdes_multi_methods(gene_values, cdf_list, displacements_list):
    """
    For each binarization method,compute P0,P1,PNA for each gene point and average across methods.

    Args:
      gene_values: 1D array of expression values for one gene
      cdfdisplacements_list: list of PDFs functions (for each binarization method)
      displacements_list: list of scalars (one displacement per binarization method) OR single scalar (applied to all)

    Returns:
      avg_probs: shape (n_points, 3) with columns [P0, P1, PNA] averaged across methods
    """
    gene_values = np.asarray(gene_values)
    n_points = gene_values.shape[0]
    n_methods = len(displacements_list)

    # allow single displacement scalar or list per method
    if np.isscalar(displacements_list):
        displacements = [displacements_list] * n_methods
    else:
        displacements = list(displacements_list)
        if len(displacements) != n_methods:
            raise ValueError("displacements_list length must equal thresholds_samples_list length")

    probs_all = np.zeros((n_methods, n_points, 3), dtype=float)

    for m, (cdf, d) in enumerate(zip(cdf_list, displacements)):
        for i, g in enumerate(gene_values):
            lower = g - d
            upper = g + d
            cdf_lower = float(cdf(lower))
            cdf_upper = float(cdf(upper))
            P1 = cdf_lower                 # P(T < g - d)
            P0 = 1.0 - cdf_upper           # P(T > g + d)
            PNA = max(0.0, cdf_upper - cdf_lower)  # middle mass
            # numerical safety
            P0, P1, PNA = np.clip([P0, P1, PNA], 0.0, 1.0)
            # ensure sum <= 1 (floating rounding)
            s = P0 + P1 + PNA
            if s > 1.0:
                # renormalize proportionally
                P0, P1, PNA = (P0/s, P1/s, PNA/s)
            probs_all[m, i] = [P0, P1, PNA]

    # average across methods
    avg_probs = probs_all.mean(axis=0)
    return avg_probs


# -------------------------------
# 2b: Conditional MAP with threshold and probability output
# -------------------------------
def conditional_map_impute_with_threshold_probs(prob_matrix, ternary_vector, p_thresh):
    """
    Impute NA points using conditional MAP with confidence threshold. Look up prob matrix for max prob value.
    Returns:
        - imputed_vector: 0/1/NA
        - imputed_probs: probability of the value for each position
    """
    ternary_vector = np.array(ternary_vector, dtype=object)
    n = len(ternary_vector)
    na_idx = [i for i, v in enumerate(ternary_vector) if v is np.nan]
    
    if not na_idx:
        probs = np.zeros(n)
        for i, val in enumerate(ternary_vector):
            probs[i] = prob_matrix[int(val)]
        return ternary_vector.copy(), probs
    
    max_prob = np.max(prob_matrix, axis=1)
    max_ind = np.argmax(prob_matrix, axis=1)
    #print(max_prob, max_ind)
    
    # Fill NAs with values if probability exceeds threshold
    imputed_vector = ternary_vector.copy()
    imputed_probs = np.zeros(n)
    
    for idx in na_idx:
        if max_prob[idx] >= p_thresh:
            imputed_vector[idx] = max_ind[idx]
            imputed_probs[idx] = max_prob[idx]
        else:
            imputed_probs[idx] = prob_matrix[idx,2]
    
    imputed_vector = np.where(imputed_vector ==2,np.nan,imputed_vector)
    
    # Fill observed positions
    for i, val in enumerate(ternary_vector):
        if i not in na_idx:
            imputed_probs[i] = prob_matrix[i,int(val)]
    
    return imputed_vector, imputed_probs


########### MADE CHANGES

# -------------------------------
# 3: Full gene matrix pipeline with probability output
# -------------------------------
def binarize_and_impute_matrix_with_probs_multi_methods(gene_matrix, cdf_list,thresholds_list, displacements_list, p_thresh, typeReturn):
    """
    Input:
        gene_matrix: 2D array-like, shape (n_genes, n_samples)
        cdf_list: list of thresholds PDF functions (one per method)
        thresholds_list: list of thresholds (one per method)
        displacements_list: list of displacements (one per method)
        p_thresh: confidence threshold for imputation
    Output:
        - imputed_matrix: same shape, 0/1 with NAs remaining if MAP < p_thresh
        - probability_matrix: probability of each imputed value
    """
    gene_matrix = np.array(gene_matrix)
    n_genes, n_samples = gene_matrix.shape
    imputed_matrix = np.zeros_like(gene_matrix, dtype=object)
    probability_matrix = np.zeros_like(gene_matrix, dtype=float)

    for i in range(n_genes):
        gene_values = gene_matrix[i]

        ######### NEW (MAKES PROB MATRIX OF OG STRING)
        probs = compute_probs_from_threshold_kdes_multi_methods(gene_values, cdf_list, displacements_list)

        ######## NEW (MULTIPLY PROB)
        p = []

        # 1: Binarization using rules from threshold/displacement
        ###### Added new elected alg
        ternary_vector = election_strings(gene_values, thresholds_list, displacements_list)

        for j, e in enumerate(ternary_vector):
          if e == 1:
            p.append(probs[j,1])
          elif e == 0:
            p.append(probs[j,0])
          else:
            p.append(probs[j,2])

        ternary_vector = np.array(ternary_vector, dtype=object)
        #print(ternary_vector, np.prod(p), p)

        # 2: Point-specific continuous probabilities averaged over all methods
        prob_matrix = compute_probs_from_threshold_kdes_multi_methods(gene_values, cdf_list, displacements_list)

        # 3: Conditional with threshold and probability
        # imputed_vector, imputed_probs = conditional_map_impute_with_threshold_probs_all(
        #     prob_matrix, ternary_vector, p_thresh
        # )

        ########### NEW (VERIFY IF TERNARY STRING HAS NAN)
        
        if typeReturn == 1:
            
            return ternary_vector, p
        
        elif typeReturn == 2: 
            
            #print(prob_matrix, ternary_vector, p_thresh)
            
            #print("error")
            #print(probs)
            
            #print(prob_matrix)
            
            imputed_vector, imputed_prob = impute_all_string_with_threshold_probs(prob_matrix, ternary_vector, p_thresh)
            
            return ternary_vector, p, imputed_vector, imputed_prob
            
        else:

            if np.isnan(list(ternary_vector)).any():

                imputed_vector, imputed_probs = conditional_map_impute_with_threshold_probs(
                    prob_matrix, ternary_vector, p_thresh
                )
                imputed_matrix[i] = imputed_vector
                probability_matrix[i] = imputed_probs

            else:
                imputed_matrix[i] = ternary_vector
                probability_matrix[i] = p

            return imputed_matrix[0], np.prod(probability_matrix), probability_matrix
        
def generateCDF():
    
    # read displacement table
    #displacements = pd.read_csv("./displacements/Displacements.csv")

    thrs = pd.read_csv('./statistics_methods/thrs.csv')
        
    thrsBasc = list(thrs['basca'].values)
    thrsOnestep = list(thrs['onestep'].values)
    thrsKmeans = list(thrs['kmeans'].values)
    thrsShmulevich = list(thrs['shmulevich'].values)
        
    cdfBasc = build_kde_cdf(thrsBasc)
    cdfOnestep = build_kde_cdf(thrsOnestep)
    cdfKmeans = build_kde_cdf(thrsKmeans)
    cdfShmulevich = build_kde_cdf(thrsShmulevich)

    cdf_dict = {'BASC A':cdfBasc, 'K-Means':cdfKmeans, 'Onestep': cdfOnestep, 'Shmulevich': cdfShmulevich}
    
    return cdf_dict


"""
if __name__ == "__main__":
    
    thrs = pd.read_csv('thrs.csv')
    
    thrsBasc = list(thrs['basca'].values)
    thrsOnestep = list(thrs['onestep'].values)
    thrsKmeans = list(thrs['kmeans'].values)
    thrsShmulevich = list(thrs['shmulevich'].values)
    
    gene = [0.19709, 0.325998, 0.155108, 0.0736089, 0.073398]
    
    cdfBasc = build_kde_cdf(thrsBasc)
    cdfOnestep = build_kde_cdf(thrsOnestep)
    cdfKmeans = build_kde_cdf(thrsKmeans)
    cdfShmulevich = build_kde_cdf(thrsShmulevich)
    
    gene = [0.75667941, 0.69192662, 0.69460907, 0.62390934, 0.69901525, 0.71149057, 0.71366999] 
    print(binarize_and_impute_matrix_with_probs_multi_methods([gene], [cdfBasc],[0.6735255385763739],[0.0306],0.5,3), "\n")
    
    # shmulevich

    print(binarize_and_impute_matrix_with_probs_multi_methods([gene], [cdfShmulevich],[0.155108],[0.0699],0.5,1), "\n")
    
    # basc

    print(binarize_and_impute_matrix_with_probs_multi_methods([gene], [cdfBasc],[0.114358],[0.0580],0.5,1), "\n")
    
    # onestep

    print(binarize_and_impute_matrix_with_probs_multi_methods([gene], [cdfOnestep],[0.225400],[0.0508],0.5,1), "\n")
    
    # kmeans

    print(binarize_and_impute_matrix_with_probs_multi_methods([gene], [cdfKmeans],[0.225400],[0.0252],0.5,1), "\n")
    
    # shmulevich, basca

    print(binarize_and_impute_matrix_with_probs_multi_methods([gene], [cdfShmulevich, cdfBasc],[0.155108, 0.114358],[0.0699, 0.0580],0.5,1), "\n")

    # basc, onestep, kmeans

    print(binarize_and_impute_matrix_with_probs_multi_methods([gene], [cdfBasc, cdfOnestep, cdfKmeans],[0.114358, 0.225400, 0.225400],[0.0580, 0.0508, 0.0252],0.5,1), "\n")

    # Elected

    print(binarize_and_impute_matrix_with_probs_multi_methods([gene], [cdfShmulevich, cdfBasc, cdfOnestep, cdfKmeans],[0.155108, 0.114358, 0.225400, 0.225400],[0.0699, 0.0580, 0.0508, 0.0252],0.5,1), "\n")
"""