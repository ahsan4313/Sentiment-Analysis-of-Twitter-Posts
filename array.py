import numpy as np
from scipy.misc import comb

# There is a comb function for Python which does 'n choose k'                                                                                            
# only you can't apply it to an array right away                                                                                                         
# So here we vectorize it...                                                                                                                             
def myComb(a,b):
  return comb(a,b,exact=True)

vComb = np.vectorize(myComb)

def get_tp_fp_tn_fn(cooccurrence_matrix):
  tp_plus_fp = vComb(cooccurrence_matrix.sum(0, dtype=int),2).sum()
  tp_plus_fn = vComb(cooccurrence_matrix.sum(1, dtype=int),2).sum()
  tp = vComb(cooccurrence_matrix.astype(int), 2).sum()
  fp = tp_plus_fp - tp
  fn = tp_plus_fn - tp
  tn = comb(cooccurrence_matrix.sum(), 2) - tp - fp - fn

  return [tp, fp, tn, fn]

if __name__ == "__main__":
  # The co-occurrence matrix from example from                                                                                                           
  # An Introduction into Information Retrieval (Manning, Raghavan & Schutze, 2009)                                                                       
  # also available on:                                                                                                                                   
  # http://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html                                                                     
  #                                                                                                                                                      
  cooccurrence_matrix = np.array([[ 5,  1,  2], [ 1,  4,  0], [ 0,  1,  3, 5]])

  # Get the stats                                                                                                                                        
  tp, fp, tn, fn = get_tp_fp_tn_fn(cooccurrence_matrix)

  print "TP: %d, FP: %d, TN: %d, FN: %d" % (tp, fp, tn, fn)

  # Print the measures:                                                                                                                                  
  print "Rand index: %f" % (float(tp + tn) / (tp + fp + fn + tn))

  precision = float(tp) / (tp + fp)
  recall = float(tp) / (tp + fn)

  print "Precision : %f" % precision
  print "Recall    : %f" % recall
  print "F1        : %f" % ((2.0 * precision * recall) / (precision + recall))