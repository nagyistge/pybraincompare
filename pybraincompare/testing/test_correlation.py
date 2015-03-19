#!/usr/bin/python

"""
Test regional and whole brain correlation scores
"""
from pybraincompare.testing.testing_functions import generate_thresholds, calculate_pybraincompare_pearson
from pybraincompare.mr.datasets import get_pair_images, get_data_directory
from pybraincompare.compare.mrutils import resample_images_ref, make_binary_deletion_mask, do_mask
from numpy.testing import assert_array_equal, assert_almost_equal, assert_equal
from pybraincompare.compare.maths import calculate_pairwise_correlation
from nose.tools import assert_true, assert_false
from pybraincompare.compare import compare, atlas as Atlas
from nilearn.image import resample_img
from pybraincompare.template.visual import view
from scipy.stats import norm, pearsonr
from pybraincompare.testing import testing_functions
import nibabel
import random
import pandas
import numpy
import os

def setup_func():
  thresholds = [0.0,0.5,1.0,1.5,1.96,2.0]
  mr_directory = get_data_directory()

  # Use 8mm resampled images for speed
  images = get_pair_images(voxdims=["8","8"])   
  standard = "%s/MNI152_T1_2mm_brain_mask.nii.gz" %(mr_directory)
  return thresholds,images,standard


# https://github.com/NeuroVault/NeuroVault/issues/133#issuecomment-74464393
'''Test that pybraincompare returns same simulated correlations'''
def test_simulated_correlations():

  # Get standard brain mask
  thresholds,images,standard = setup_func()

  # Generate random data inside brain mask, run 10 iterations
  standard = nibabel.load(standard)
  number_values = len(numpy.where(standard.get_data()!=0)[0])
  numpy.random.seed(9191986)
  for x in range(0,10):  
    data1 = norm.rvs(size=number_values)
    data2 = norm.rvs(size=number_values)
    corr = pearsonr(data1,data2)[0]
      
    # Put into faux nifti images
    mr1 = numpy.zeros(standard.shape)
    mr1[standard.get_data()!=0] = data1
    mr1 = nibabel.nifti1.Nifti1Image(mr1,affine=standard.get_affine(),header=standard.get_header())
    mr2 = numpy.zeros(standard.shape)
    mr2[standard.get_data()!=0] = data2
    mr2 = nibabel.nifti1.Nifti1Image(mr2,affine=standard.get_affine(),header=standard.get_header())  
    score = calculate_pybraincompare_pearson([mr1,mr2])  
    assert_almost_equal(corr,score,decimal=5)
