-   [Introduction](#introduction)
-   [Classic Computer vision techniques - White box algorithms](#classic-computer-vision-techniques---white-box-algorithms)
    -   [Step 1 - Key Point Detection](#step-1---key-point-detection)
    -   [Step 2 - Descriptor Extraction](#step-2---descriptor-extraction)
    -   [Step 3 - Matching](#step-3---matching)
    -   [Step 4 - Model Fitting](#step-4---model-fitting)
-   [Standard algorithms](#standard-algorithms)
    -   [SIFT- Scale Invariant Feature Transform](#sift--scale-invariant-feature-transform)
    -   [SURF – Speeded-Up Robust Features](#surf-speeded-up-robust-features)
    -   [U-SURF – Upright-SURF](#u-surf)
    -   [BRIEF – Binary Robust Independent Elementary Features](#brief-binary-robust-independent-elementary-features)
    -   [R-BRIEF – Rotation (?) BRIEF](#rbrief)
    -   [CenSurE](#censure)
    -   [ORB – Oriented FAST and Rotated BRIEF](#orb-oriented-fast-and-rotated-brief)
    -   [KASE - ](#kase--)
    -   [FAST – Features from Accelerated Segment Test](#fast-features-from-accelerated-segment-test)
    -   [Delaunay Graph Matching](#delaunay-graph-matching)
-   [Hash algorithms](#hash-pictures)
    -   [A-HASH : Average Hash](#ahash)
    -   [D-HASH](#dhash)
    -   [P-HASH](#phash)
    -   [R-HASH](#rhash)
    -   [Spectral-HASH](#spectral-hash)
    -   [E2LSH - LSH - Locality Sensitve Hashing](#E2LSH)
-   [Neural networks – Black box algorithms](#neural-networks-black-box-algorithms)
    -   [RBM - Restricted Boltzmann machine](#rbm)
    -   [RPA - Robust Projection Algorith](#rpa)
    -   [Boosting SSC](#bssc)
    -   [ConvNet - Convolutional Neural Networks](#convnet---convolutional-neural-networks)

Introduction
============

A general overview was made through standard web lookup. \[3\] A look was given to libraries, which also provide detailed and useful information. \[15\]

In the following, we expose :

-   The main steps of a Image Matching algorithm

-   Few of the most popular Image Matching algorithms

Please, be sure to consider this document is under construction, and it can contain mistakes, structural errors, missing areas .. feel free to ping me if you find such flaw. (Open a PR/Issue/...)

Classic Computer vision techniques - White box algorithms
=========================================================

Step 1 - Key Point Detection
----------------------------

-   Corner detectors to find easily localizable points.

#### Harris

\[6\]

Distinctive features :

-   Rotation-invariant

-   NOT scaling invariant

#### FAST

Distinctive features :

-   Not rotation-invariant (no orientation calculation)

-   ? scaling invariant

Step 2 - Descriptor Extraction
------------------------------

Extract a small patch around the keypoints, preserving the most relevant information and discaring necessary information (illumination ..)

Can be :

-   Pixels values

-   Based on histogram of gradient

-   Learnt

Usually :

-   Normalized

-   Indexed in a searchable data structure

##### Example

Vector descriptors based on our keypoints, each descriptor has size 64 and we have 32 such, so our feature vector is 2048 dimension.

##### Descriptor’s quality

A good descriptor code would be, according to \[16\] :

-   easily computed for a novel input

-   requires a small number of bits to code the full dataset

-   maps similar items to similar binary codewords

-   require that each bit has a 50

We should be aware that a smaller code leads to more collision in the hash.

Step 3 - Matching
-----------------

Linked to correspondence problem ?

### Distance

#### Hamming distance

#### Bruteforce

-   *O*(*N*<sup>2</sup>), N being the number of descriptor per image

-   One descriptor of the first picture is compared to all descriptor of a second candidate picture. A distance is needed. The closest is the match.

-   Ratio test

-   CrossCheck test : list of “perfect match” (TO CHECK)

#### Best match

-   Returns only the best match

-   Returns the K (parameter) best matchs

#### FLANN – Fast Library for Approximate Nearest Neighboors

-   Collections of algorithm, optimized for large dataset/high dimension

-   Returns the K (parameter) best matchs

-   \[17\]

### Compression of descriptors before matching

#### LSH – Locally Sensitive Hashing

-   O(~N)

-   Returns the K (parameter) best matchs

-   \[17\]

-   Convert descriptor (floats) to binary strings. Binary strings matched with Hamming Distance, equivalent to a XOR and bit count (very fast with SSE instructions on CPU)

#### BBF – Best bin first Kd-tree

-   O(~N)

-   Example : SIFT – Scale Invariant Feature Tranform

Step 4 - Model Fitting
----------------------

-   Identify inliers and outliers ~ Fitting a homography matrix ~ Find the transformation of (picture one) to (picture two)

-   Inliers : “good” points matching that can help to find the transformation

-   outliers : “bad” points matching

-   See \[15\]

#### RANSAC – Random Sample Consensus

Estimation of the homography

#### Least Meadian

Standard algorithms
===================

Goal is to transform visual information into vector space

SIFT- Scale Invariant Feature Transform
---------------------------------------

From the original paper \[8\] and a concise explanation from \[13\]

#### Pro

-   test

#### Con

-   and not included in OpenCV (only non-free module)

-   Slow (HOW MUCH TO CHECK)

#### Steps of the algorithm

1.  Extrema detection

    Uses an approximation of LoG (Laplacian of Gaussian), as a Difference of Gaussion, made from difference of Gaussian blurring of an image at different level of a Gaussian Pyramid of the image. Kept keypoints are local extrema in the 2D plan, as well as in the blurring-pyramid plan.

2.  Keypoint localization and filtering

    Two threesholds has to be set :

    -   Contract Threeshold : Eliminate low contract keypoint ( 0.03 in original paper)

    -   Edge Threeshold : Eliminate point with a curvature above the threeshold, that could match edge only. (10 in original paper)

3.  Orientation assignement

    Use an orientation histogram with 36 bins covering 360 degrees, filled with gradient magnitude of given directions. Size of the windows on which the gradient is calculated is linked to the scale at which it’s calculated. The average direction of the peaks above 80% of the highest peak is considered to calculate the orientation.

4.  Keypoint descriptors

    A 16x16 neighbourhood around the keypoint is divided into 16 sub-blocks of 4x4 size, each has a 8 bin orientation histogram. 128 bin are available for each Keypoint, represented in a vector of float, so 512 bytes per keypoint. Some tricks are applied versus illumination changes, rotation.

5.  Keypoint Matching

    Two distance calculation :

    -   Finding nearest neighboor.

    -   Ratio of closest distance to second closest is taken as a second indicator when second closest match is very near to the first. Has to be above 0.8 (original paper) (TO CHECK what IT MEANS)

SURF – Speeded-Up Robust Features
---------------------------------

\[2\]

#### Pro

-   Faster than SIFT (x3) : Parralelization, integral image ..

-   Tradeoffs can be made :

    -   Faster : no more rotation invariant, lower precision (dimension of vectors)

    -   More precision : **extended** precision (dimension of vectors)

-   Good for blurring, rotation

#### Con

-   -   Not good for illumination change, viewpoint change

#### Steps of the algorithm

1.  Extrema detection

    Approximates Laplacian of Guassian with a Box Filter. Computation can be made in parrallel at different scales at the same time, can use integral images … Roughly, does not use a gaussian approximation, but a true “square box” for edge detection, for example.

    The sign of the Laplacian (Trace of the Hessian) give the “direction” of the contrast : black to white or white to black. So a negative picture can match with the original ? (TO CHECK)

2.  Keypoint localization and filtering

3.  Orientation assignement

    Dominant orientation is computed with wavlet responses with a sliding window of 60

4.  Keypoint descriptors

    Neighbourhood of size 20sX20s is taken around the keypoint, divided in 4x4 subregions. Wavelet response of each subregion is computed and stored in a 64 dimensions vector (float, so 256 bytes), in total. This dimension can be lowered (less precise, less time) or extended (e.g. 128 bits ; more precise, more time)

5.  Keypoint Matching

U-SURF – Upright-SURF
---------------------

Rotation invariance can be “desactivated” for faster results, by bypassing the main orientation finding, and is robust up to 15rotation.

BRIEF – Binary Robust Independent Elementary Features
-----------------------------------------------------

Extract binary strings equivalent to a descriptor without having to create a descriptor

See BRIEF \[18\]

#### Pro

-   Solve memory problem

#### Con

-   Only a keypoint descriptor method, not a keypoint finder

-   Bad for large in-plan rotation

#### Steps of the algorithm

1.  Extrema detection

2.  Keypoint localization and filtering

3.  Orientation assignement

4.  Keypoint descriptors

    Compare pairs of points of an image, to directly create a bitstring of size 128, 256 ou 512 bits. (16 to 64 bytes)

    Each bit-feature (bitstring) has a large variance ad a mean near 0.5 (TO VERIFY). The more variance it has, more distinctive it is, the better it is.

5.  Keypoint Matching Hamming distance can be used on bitstrings.

R-BRIEF – Rotation (?) BRIEF
----------------------------

Variance and mean of a bit-feature (bitstring) is lost if the direction of keypoint is aligned (TO VERIFY : would this mean that there is a preferential direction in the pair of point selection ? )

Uncorrelated tests (TO CHECK WHAT IT IS) are selected to ensure a high variance.

CenSurE
-------

#### Pro

#### Con

ORB – Oriented FAST and Rotated BRIEF
-------------------------------------

From \[10\] which is rougly a fusion of FAST and BRIEF. See also \[14\]

#### Pro

-   Not patented

#### Con

#### Steps of the algorithm

1.  Extrema detection

    FAST algorithm (no orientation)

2.  Keypoint localization and filtering

    Harris Corner measure : find top N keypoints

    Pyramid to produce multi scale features

3.  Orientation assignement

    The direction is extracted from the orientation of the (center of the patch) to the (intensity-weighted centroid fo the patch). The region/patch is circular to improve orientation invariance.

4.  Keypoint descriptors

    R-BRIEF is used, as Brief Algorithm is bad at rotation, on rotated patches of pixel, by rotating it accordingly with the previous orientation assignement.

5.  Keypoint Matching

    Multi-probe LSH (improved version of LSH)

KASE - 
-------

Shipped in OpenCV library. Example can be found at \[9\]

#### Pro

#### Con

#### Steps of the algorithm

FAST – Features from Accelerated Segment Test
---------------------------------------------

#### Pro

#### Con

#### Steps of the algorithm

1.  Extrema detection

2.  Keypoint localization and filtering

3.  Orientation assignement

4.  Keypoint descriptors

5.  Keypoint Matching

Delaunay Graph Matching
-----------------------

Algorithm from 2012, quite advanced. Would need some tests or/and review See M1NN \[4\] that is presenting 3 algorithms :

- **M1NN Agglomerative Clustering**
Different types of data,robust to noise, may ’over’ cluster. Better clustering performance and is extendable to many applications, e.g. data mining, image segmentation and manifolding learning.

- **Modified Log-likelihood Clustering**
Measure and compare clusterings quantitatively and accurately. Energy of a graph to measure the complexity of a clustering.

- **Delaunay Graph Characterization and Graph-Based Image Matching**
Based on diffusion process and Delaunay graph characterization, with critical time. Graph-based image matching method. SIFT descriptors also used. Outperforms SIFT matching method by a lower error rate.

#### Pro

-   Lower error

-   Extensible to 3D (but not done yet ?)

#### Con

-   Lower number of matches

#### Steps of the algorithm

Hash algorithms
===============

The following algorithms does not intend to match pictures with common part, but to match pictures which are rougly the same. To be clear : If the hashes are different, then the data is different. And if the hashes are the same, then the data is likely the same. There is a possibility of a hash collision, having the same hash values then does not guarantee the same data.

A-HASH : Average Hash
---------------------

From ... \[11\]

“the result is better than it has any right to be.”

relationship between parts of the hash and areas of the input image = ability to apply “masks” (like "ignore the bottom 25 8 bits for a image vector.

Idea to be faster (achieve membw-bound conditions) : Batch search (compare more than one vector to all others) = do X search at the same time

More than one vector could be transformation of the initial image (rotations, mirrors)

Javascript Implementation : \[1\]

#### Pro

-   Masks and transformation available

-   Ability to look for modified version of the initial picture

-   Only 8 bits for a image vector.

#### Con

-   Nd

#### Steps of the algorithm

1.  Ce

D-HASH
------

From \[5\], DHash is a very basic algorithm to find nearly duplicate pictures. The hash can be of length 128 or 512 bits. The delta between 2 “matches” is a Hamming distance (\# of different bits.)

#### Pro

-   Detecting near or exact duplicates : slightly altered lighting, a few pixels of cropping, or very light photoshopping

#### Con

-   Not for similar images

-   Not for duplicate-but-cropped

#### Steps of the algorithm

1.  Convert the image to grayscale

2.  Downsize it to a 9x9 thumbnail

3.  Produce a 64-bit “row hash”: a 1 bit means the pixel intensity is increasing in the x direction, 0 means it’s decreasing

4.  Do the same to produce a 64-bit “column hash” in the y direction

5.  Combine the two values to produce the final 128-bit hash value

P-HASH
------

From ... \[11\] Exist in mean and median flavors

8 bits for a image vector. Java implementation : \[12\]

#### Pro

-   Robustness to gamma

-   Robustness to color histogram adjustments

#### Con

-   Nd

#### Steps of the algorithm

1.  Reduce size of the input image to 32x32 (needed to simplify DCT computation)

2.  Reduce color to grayscale (same)

3.  Compute the DCT : convert image in frequencies, a bit similar to JPEG compression

4.  Reduce the DCT : keep the top-left 8x8 of the DCT, which are the lowest frequencies

5.  Compute the average DCT value : without the first term (i.e. solid colors)

6.  Further reduce the DCT : Set the 64 hash bits to 0 or 1 depending on whether each of the 64 DCT values is above or below the average value.

7.  Construct the hash : create a 64 bits integer from the hash

8.  Comparing with Hamming Distance (threeshold = 21)

R-HASH
------

From ... \[11\]

Equivalent to A-Hash with more granularity of masks and transformation. Ability to apply “masks” (color channel, ignoring (f.ex. the lowest two) bits of some/all values) and “transformations” at comparison time. (color channel swaps)

48 bits for a rgb image vector

#### Pro

-   Masks and transformation available

-   More precise masks (than A-hash)

-   More precise transformations (than A-hash)

#### Con

-   Larger memory footprint

#### Steps of the algorithm

1.  Image scaled to 4x4

2.  Compute vector

3.  Comparison = sum of absolute differences: abs(a\[0\]-b\[0\]) + abs(a\[1\]-b\[1\]) + ... + abs(a\[47\]-b\[47\]) = 48 dimensional manhattan distance

Spectral-HASH
-------------

From \[16\]. A word is given in \[11\]

The bits are calculated by thresholding a subset of eigenvectors of the Laplacian of the similarity graph

Similar performance to RBM

![Spectral Hashing comparison from \[16\] <span data-label="fig:spectral_hashing_comparison"></span>](sota-ressources/spectral_hashing_comparison.png)

#### Pro

-   D

#### Con

-   Nd

#### Steps of the algorithm

1.  Ce

E2LSH - LSH - Locality Sensitve Hashing
---------------------------------------

From ... A word is given in \[16\] The code is calculated by a random linear projection followed by a random threshold, then the Hamming distance between codewords will asymptotically approach the Euclidean distance between the items.

Not so far from Machine Learning Approaches, but outperformed by them.

#### Pro

-   Faster than Kdtree

#### Con

-   Very inefficient codes (512 bits for a picture (TO CHECK))

#### Steps of the algorithm

1.  Ce

Neural networks – Black box algorithms
======================================

RBM - Restricted Boltzmann machine
----------------------------------

From ... A word is given in \[16\]

To learn 32 bits, the middle layer of the autoencoder has 32 hidden units Neighborhood Components Analysis (NCA) objective function = refine the weights in the network to preserve the neighborhood structure of the input space.

#### Pro

-   More compact outputs code of picture than E2LSH = Better performances

#### Con

-   e

#### Steps of the algorithm

1.  Ce

RPA - Robust Projection Algorith
--------------------------------

From ... \[7\]

#### Pro

-   M

#### Con

-   e

#### Steps of the algorithm

1.  R

Boosting SSC
------------

From ... A word is given in \[16\]

#### Pro

-   Better than E2LSH

#### Con

-   Worst than RBM

#### Steps of the algorithm

1.  Ce

ConvNet - Convolutional Neural Networks
---------------------------------------

Learn a metric between any given two images. The distance can be threesholded to decide if images match or not.

#### Training phase

Goal :

-   Minimizing distance between “same image” examples

-   Maximizing distance between “not same image” examples

#### Evaluation phase

Apply an automatic threeshold.

##### SVM - Support Vector Machine

1. Valentino Aluigi. 2019. JavaScript implementation of the Average Hash using HTML5 Canvas.

2. Herbert Bay, Tinne Tuytelaars, and Luc Van Gool. 2006. SURF: Speeded Up Robust Features. In *Computer Vision 2006*, Aleš Leonardis, Horst Bischof and Axel Pinz (eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 404–417. <https://doi.org/10.1007/11744023_32>

3. Chomba Bupe. 2017. What algorithms can detect if two images/objects are similar or not? - Quora.

4. Yan Fang. 2012. Data Clustering and Graph-Based Image Matching Methods.

5. Nicolas Hahn. 2019. Differentiate images in python: Get a ratio or percentage difference, and generate a diff image - nicolashahn/diffimg.

6. C. Harris and M. Stephens. 1988. A Combined Corner and Edge Detector. In *Procedings of the Alvey Vision Conference 1988*, 23.1–23.6. <https://doi.org/10.5244/C.2.23>

7. Igor. 2011. Nuit Blanche: Are Perceptual Hashes an instance of Compressive Sensing ? *Nuit Blanche*.

8. David G. Lowe. 2004. Distinctive Image Features from Scale-Invariant Keypoints. *International Journal of Computer Vision* 60, 2: 91–110. <https://doi.org/10.1023/B:VISI.0000029664.99615.94>

9. Andrey Nikishaev. 2018. Feature extraction and similar image search with OpenCV for newbies. *Medium*.

10. Ethan Rublee, Vincent Rabaud, Kurt Konolige, and Gary Bradski. 2011. ORB: An efficient alternative to SIFT or SURF. In *2011 International Conference on Computer Vision*, 2564–2571. <https://doi.org/10.1109/ICCV.2011.6126544>

11. 2011. Looks Like It - The Hacker Factor Blog.

12. 2011. pHash-like image hash for java. *Pastebin.com*.

13. 2014. Introduction to SIFT (Scale-Invariant Feature Transform) 3.0.0-dev documentation.

14. 2014. ORB (Oriented FAST and Rotated BRIEF) 3.0.0-dev documentation.

15. Feature Matching + Homography to find Objects 3.0.0-dev documentation.

16. Spectralhashing.Pdf.

17. OpenCV: Feature Matching.

18. BRIEF (Binary Robust Independent Elementary Features) 3.0.0-dev documentation.