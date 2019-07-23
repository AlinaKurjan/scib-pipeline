#!/bin/env python

### D. C. Strobl, M. Müller; 2019-07-23

""" This module provides a toolkit for running a large range of single cell data integration methods
    as well as tools and metrics to benchmark them.
"""

import scanpy as sc
import anndata
import numpy as np

# first, some checker functions for data sanity
def checkAdata(adata):
    if type(adata) is not anndata.AnnData:
        raise TypeError('Input is not a valid AnnData object')

def checkBatch(batch, obs):
    if batch not in obs:
        raise ValueError('Selected batch column is not in obs')
    else:
        nBatch = obs[batch].nunique()
        print('Object contains '+str(nBatch)+' batches.')

def splitBatches(adata, batch):
    split = []
    for i in adata.obs[batch].unique():
        split.append(adata[adata.obs[batch]==i])
    return split


# functions for running the methods

def runScanorama(adata, batch, hvgPre):
    import scanorama
    checkAdata(adata)
    checkBatch(batch, adata.obs)
    split = splitBatches(adata.copy(), batch)
    emb, corrected = scanorama.correct_scanpy(split, return_dimred=True)
    corrected = corrected[0].concatenate(corrected[1:])
    emb = np.concatenate(emb, axis=0)

    return emb, corrected

def runScGen(adata, cell_type='louvain', batch='method', model_path='./models/batch', epochs=100):
    if 'cell_type' not in adata.obs:
        adata.obs['cell_type'] = adata.obs[cell_type].copy()
    if 'batch' not in adata.obs:
        adata.obs['batch'] = adata.obs[batch].copy()
    
    # TODO: reduce data
        
    network = scgen.VAEArith(x_dimension= adata.shape[1], model_path=model_path)
    network.train(train_data=adata, n_epochs=epochs)
    corrected_adata = scgen.batch_removal(network, adata)
    network.sess.close()
    return corrected_adata

if __name__=="__main__":
    adata = sc.read('testing.h5ad')
    emb, corrected = runScanorama(adata, 'method', False)
    print(emb)
    print(corrected)


        

