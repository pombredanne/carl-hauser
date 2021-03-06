-   [Introduction](#introduction)
    -   [Goal](#goal)
    -   [Methodology](#methodology)
    -   [Problem Statement](#problem-statement)
-   [Classic Computer vision techniques - White box algorithms](#classic-computer-vision-techniques---white-box-algorithms)
    -   [Structure of Classic vision techniques](#structure-of-classic-vision-techniques)
    -   [Step 1 - Key Point Detection](#step-1---key-point-detection)
    -   [Step 2 - Descriptor Extraction](#step-2---descriptor-extraction)
    -   [Step 3 - Feature representation](#feature-representation)
    -   [Step 4 - Matching](#step-3---matching)
    -   [Step 5 - Model Fitting](#step-4---model-fitting)
-   [Global Features Algorithms](#standard-algorithms)
    -   [Overview](#overview)
    -   [Categories](#categories)
    -   [Full region features - FH or CTPH - Fuzzy Hashing Algorithms](#full-region-features---fh-or-ctph---fuzzy-hashing-algorithms)
    -   [Per subregion features](#per-subregion-features)
-   [Algorithms combination](#algorithms-combination)
    -   [Phishing](#phishing)
    -   [Non-Specific](#non-specific)
-   [Local Features Algorithms](#standard-algorithms)
    -   [Comparison overview](#comparison-overview)
    -   [Non-binary features](#non-binary-features)
    -   [Binary features](#binary-features)
    -   [Unsorted](#unsorted)
-   [Neural networks – Black box algorithms](#neural-networks-black-box-algorithms)
    -   [FAST – Features from Accelerated Segment Test](#fast-features-from-accelerated-segment-test)
    -   [CNN - Convolutional Neural Network](#cnn---convolutional-neural-network)
    -   [FRCNN - Faster RCNN](#frcnn)
    -   [RTSVMs - Robust Transductive Support Vector Machines](#rtsvms---robust-transductive-support-vector-machines)
    -   [RBM - Restricted Boltzmann machine](#rbm)
    -   [RPA - Robust Projection Algorith](#rpa)
    -   [Boosting SSC](#bssc)
    -   [ConvNet - Convolutional Neural Networks](#convnet---convolutional-neural-networks)
-   [Utility algorithms](#utilities-algorithms)
    -   [SWS - Sliding Windows Search](#sws)
    -   [ESS - Efficient Subwindow Search](#ess)
    -   [SLICO - Simple Linear Iterative Clustering](#slico)
    -   [HSNW - ... indexing](#hsnw---...-indexing)
    -   [Raw results](#raw-results)

Introduction
============

##### Goal

The goal of this document is to provide an overview of the tools and ideas to cluster similar pictures or pictures with similar elements together. This document intents to provide State-of-the-art references, as well as library tests and results review. It may also give insights about combinaison or ideas to improve found ideas.

##### Methodology

A general overview was made through standard web lookup. \[8\] A look was given to libraries, which also provide detailed and useful information. \[53\]

In the following, we expose :

-   The main steps of a Image Matching algorithm

-   Few of the most popular Image Matching algorithms

##### Problem Statement

\[9\] states the Image Retrieval problem as “Given a query image, finding and representing (in an ordered manner) the images depicting the same scene or objects in large unordered image collections”

**Please, be sure to consider this document is under construction, and it can contain mistakes, structural errors, missing areas .. feel free to ping me if you find such flaw. (Open a PR/Issue/...)**

Classic Computer vision techniques - White box algorithms
=========================================================

Correspondances can be found between pictures, and so can be used for, e.g. : \[6\]:

1.  **Similarity Measurement** : probability of two images for showing the same scene

2.  **Geometry Estimation** : estimate the transformation between two object views

3.  **Data Association** : Sorting pictures by scene (TO CHECK : Same as Similarity measurement)

Block based approach : the image is divided into various blocks. These block division is done on the basis of Discrete Wavelet Transform, Discrete Cosine Transform, Zernike moment, and Fourier Mellin Transform. \[28\]

![Image maching pipeline from \[6\] <span data-label="fig:image_matching_pipeline"></span>](sota-ressources/image-matching-pipeline.png)

#### Structure of Classic vision techniques

From \[37\] :

1.  **Global features detection**

    1.  **Full region**

    2.  **Per subregion**

2.  **Local features detection**
    Detection should be stable and repeatable. Corners, textured areas, etc. can be interest points. Robust to occlusion and viewpoint changes.

    1.  **Dense sampling over regular grid**

    2.  **Interest points detection**
        Find where interest points are.

        1.  Not robust to scale
            Examples : Harris corner detector

        2.  Robust to scale
            Examples : Not robust + Increasing Gaussian blur many time, one for each scale ; Automatic scale selection ; ...

    3.  **Exotics**

        1.  Random points sampling

        2.  Segmentation (?)

        3.  Pose estimation
            Example : “pictorial structure” (poselet) More complex

Step 1 - Key Point Detection
----------------------------

-   Corner detectors to find easily localizable points.

#### Harris Detector

From the original paper \[17\]. Based on the central principle: at a corner, the image intensity will change largely in multiple directions, with a windows shift.

(invariance to rotation, scale, illumination, noise .. said \[37\])

Distinctive features :

-   Rotation-invariant

-   NOT scaling invariant
    One point could be a corner in a small scaled neighborhood, or as an edge in a large scaled neighborhood.

#### CSS - Curvature Space Scale

#### Hit and Miss filter

#### Shi/Tomasi

#### SUSAN

From ... a word in \[29\] Less accuracy, more speed.

#### FAST - Features from Accelerated Segment Test

From the original paper \[29\] cited in \[43\]
Is a corner detector, based on machine learning. More accuracy, kept with high speed. Based on SUSAN

Distinctive features :

-   Not rotation-invariant (no orientation calculation)

-   ? scaling invariant

#### Pro

-   High repeatability

#### Con

-   not robust to high levels noise

-   can respond to 1 pixel wide lines

-   dependent on a threshold

-   no scale/rotation invariance (? TO CHECK)

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

A good descriptor code would be, according to \[54\] :

-   easily computed for a novel input

-   requires a small number of bits to code the full dataset

-   maps similar items to similar binary codewords

-   require that each bit has a 50

We should be aware that a smaller code leads to more collision in the hash.

Step 3 - Feature representation
-------------------------------

A local feature needs to be represented. From \[37\]

### Bag-Of-Words or Bag-Of-Features

From \[37\], representing an image as a set of feature descriptor.

##### Pro

-   Insensitivity of objects location in image

##### Con

-   Loss of spatial information

### Codebook Generation

From \[37\], K-Means clustering over all words describing all pictures. A representative word (=Codeword) of each cluster is chosen (the “mean word”). A list of all representative words is created. A representative vector for each image, is created, as a boolean\_list/histogram of representative words linked or not to this image.

##### Pro

-   Shorten the comparisons to do (TO CHECK)

##### Con

-   Representation ambiguity : Codeword may not be representative of a cluster of words (too large, too narrow, more than 1 meaning, ...)

### Soft Vector Quantization

From \[37\], codebook Generation with most and least frequent words removal. Each feature is then represented by a small group of codewords.

##### Pro

-   Mitigate the representation ambiguity problem of CodeBook

##### Con

-   Undo something that has been done ? TO CHECK !

### Hierarchical CodeWords

From \[37\], keep spatial information about the neighboorhood of a codeword.

### Visual sentences

Project codeword on a spatial axis. Relative spatial relation between words are kept.

### SPM - Spatial Pyramid Matching

From \[37\], divide a picture into equal partitions (/4, /8, ..), compute a Bag-Of-Word for each partition, its histogram, and concatenate them into one big “ordered” histogram.

##### Pro

-   Keep spatial information of features

##### Con

-   Some “bad translation” can occurs, and split features into different Bag-of-words.

![3 levels spatial pyramid from \[37\] <span data-label="fig:spm_figure"></span>](sota-ressources/spm.png)

### L-SPM - Latent Spatial Pyramid Matching

From \[37\], based on SPM but does not split the picture in equal partition = the cell of the pyramid is not spatially fixed.

The cells of the pyramid to move within search regions instead of a predefined rigid partition. Use ESS (See utilities)

##### Pro

##### Con

-   High computational cost

Step 4 - Matching
-----------------

Linked to correspondence problem ?

### Datastructure

Compression of descriptors before matching

#### LSH - Locally Sensitive Hashing

-   O(~N)

-   Returns the K (parameter) best matchs

-   \[55\]

-   Convert descriptor (floats) to binary strings. Binary strings matched with Hamming Distance, equivalent to a XOR and bit count (very fast with SSE instructions on CPU)

#### BBF - Best bin first Kd-tree

-   O(~N)

-   Example : SIFT – Scale Invariant Feature Tranform

### Distance

#### Hamming distance / Bruteforce

Partially solved by \[23\]
Works with binary features. Can be accelerated with GPU \[<span class="citeproc-not-found" data-reference-id="bianImageMatchingApplicationorienteda">**???**</span>\].

-   *O*(*N*<sup>2</sup>), N being the number of descriptor per image

-   One descriptor of the first picture is compared to all descriptor of a second candidate picture. A distance is needed. The closest is the match.

-   Ratio test

-   CrossCheck test : list of “perfect match” (TO CHECK)

#### FLANN - Fast Library for Approximate Nearest Neighboors

From \[<span class="citeproc-not-found" data-reference-id="bianImageMatchingApplicationorienteda">**???**</span>\], is an approximation for matching in Euclidian space, with KD-Tree techniques.
Work with non-binary features.

-   Collections of algorithm, optimized for large dataset/high dimension

-   Returns the K (parameter) best matchs

-   \[55\]

##### Implementation

Apache 2 From \[7\], available at : <https://github.com/nmslib/nmslib> \[51\] Does not benchmark memory usage.

### Selection

Higly noisy correspondences need to be filtered.

#### Best match

-   Returns only the best match

-   Returns the K (parameter) best matchs

#### RATIO - 

From \[<span class="citeproc-not-found" data-reference-id="bianImageMatchingApplicationorienteda">**???**</span>\] recognizes the distinctiveness of features by comparing the distance of their two nearest neighbors.
This test rejects poor matches by computing the ratio between the best and second-best match. If the ratio is below some threshold, the match is discarded as being low-quality.

#### GMS - Gird-based Motion Statistics

Uses the motion smoothness constraint. Equivalent to RATIO.
Robustness, accuracy, sufficiency, and efficiency of GMS all depend on the number of interest points detected.

#### QBH - Quantization Based Hashing

From \[32\] Incorporates quantization error into the conventional property preserving hashing models to improve the effectiveness of the hash codes

##### IMI - Inverted Multi-Index

##### NGS - Neighboorhood Graph Search

##### HNSW - Hierarchical Navigable Small Worlds

Graph based approach. Precise approximate nearest neighbor search in billion-sized datasets.
**Highly scalable** : “Indexing 1 billion vectors takes about 26 hours with L&C: we can add more than 10,000 vectors per second to the index. We refine at most 10 vectors.”

###### Implementation

BSD <https://github.com/facebookresearch/faiss> \[52\]

Step 5 - Model Fitting
----------------------

From \[<span class="citeproc-not-found" data-reference-id="bianImageMatchingApplicationorienteda">**???**</span>\] and \[53\], is a step where the geometry of the scene is verified and/or estimated. Given correspondances, the pose of the object is estimated.

-   Identify inliers and outliers ~ Fitting a homography matrix ~ Find the transformation of (picture one) to (picture two)

-   Inliers : “good” points matching that can help to find the transformation

-   outliers : “bad” points matching

### RANSAC - Random Sample Consensus

Estimation of the homography, searches for the best relative pose between images iteratively and removes outliers that disobey the estimated geometry relation finally. Correspondences that pass the geometry verification are named verified correspondences. Provides a robust estimation of transform matrix.

### Least Meadian

Global Features Algorithms
==========================

##### Overview

Global feature algorithms try to give a global and general descriptor for a given picture. Generally, this kind of approach is weak against some transformation as occlusion, clutter.It needs a fixed viewpoint, a clear background, an fixed pose.

The main assumption is that the similar images in the Euclidean space must have similar binary codes. \[9\]

##### Categories

-   Locality Sensitive Hashing schemes (LSH)

-   Context Triggered Piecewise Hashing (CTPH)

Full region features - FH or CTPH - Fuzzy Hashing Algorithms
------------------------------------------------------------

##### Overview

These algorithms do not intend to match pictures with common part, but to match pictures which are roughly the same or are near copies of one another.
To be clear : If the hashes are different, then the data is different. And if the hashes are the same, then the data is likely the same. There is a possibility of a hash collision, having the same hash values then does not guarantee the same data. \[31\] specify that Context Triggered Piecewise Hashing (CTPH) is a combination of Cryptographic Hashes (CH), Rolling Hashes (RH) and Piecewise Hashes (PH).

##### Misc. notes

-   Discrete Cosine Transformation (CDT) may be worst than Discrete Wavelet Transformation (DWT).

-   SDHash seesm the more accurate, but the slower. Cross-reference seems a good way to go.

##### Examples

-   Holistic features (=“Spatial enveloppe” = naturalness, openness, roughness, ruggedness, expansion ..)

-   Colors histograms

-   “Global Self-Similarity” (=spatial arrangement)

![Results of (a/b/d/m/p/w)-Hash from \[56\] - Lower score is better<span data-label="fig:tests"></span>](sota-ressources/outputs-evaluation/results_0.png)

### A-HASH : Average Hash

##### Overview

From ... \[40\] : “the result is better than it has any right to be.”

There exist relationship between parts of the hash and areas of the input image, that provide ability to apply “masks” (like “ignore the bottom 25% of the image”.) and “transformations” at comparison time. (searches for rotations in 90degree steps, mirroring, inverts...)

8 bits for a image vector.

Idea to be faster (achieve membw-bound conditions) : Batch search (compare more than one vector to all others) = do X search at the same time.

More than one vector could be transformation of the initial image (rotations, mirrors).

##### Pro

-   Masks and transformation available

-   Ability to look for modified version of the initial picture

-   Only 8 bits for a image vector.

##### Implementation

ImageHash 4.0 <https://pypi.org/project/ImageHash/>
Javascript Implementation : \[2\]

##### Results

Results given by the ImageHash implementation of A-hash algorithm does not provides reliable results.

<span>0.99</span> <img src="sota-ressources/outputs-evaluation/a-hash/false_structural_2.png" title="fig:" alt="A-hash" />

<span>0.99</span> <img src="sota-ressources/outputs-evaluation/a-hash/good_structural.png" title="fig:" alt="A-hash" />

<span>0.99</span> <img src="sota-ressources/outputs-evaluation/a-hash/false_structural.png" title="fig:" alt="A-hash" />

<span>0.99</span> <img src="sota-ressources/outputs-evaluation/a-hash/no_logo_match.png" title="fig:" alt="A-hash" />

<span>0.49</span> <img src="sota-ressources/outputs-evaluation/a-hash/true_structure.png" title="fig:" alt="A-hash" />

<span>0.45</span> <img src="sota-ressources/outputs-evaluation/a-hash/bad_matching.png" title="fig:" alt="A-hash" />

<span>0.7</span> <img src="sota-ressources/outputs-evaluation/a-hash/bad_matching_2.png" title="fig:" alt="A-hash" />

###### Time

Hashing time : 16.796968936920166 sec for 207 items (0.081s per item)
Matching time : nobs=207, minmax=(0.023s, 1.58s), mean=0.08s, variance=0.025s, skewness=6.62s, kurtosis=50.37s

### B-HASH : Block Hash

Seems worst than A-hash.

##### Implementation

\[57\] <http://blockhash.io> and <https://github.com/commonsmachinery/blockhash-python>

### D-HASH - Difference Hashing

From \[16\], DHash is a very basic algorithm to find nearly duplicate pictures.
The hash can be of length 128 or 512 bits. The delta between 2 “matches” is a Hamming distance (\# of different bits.)

##### Pro

-   Detecting near or exact duplicates : slightly altered lighting, a few pixels of cropping, or very light photoshopping

##### Con

-   Not for similar images

-   Not for duplicate-but-cropped

##### Steps of the algorithm

1.  Convert the image to grayscale

2.  Downsize it to a 9x9 thumbnail

3.  Produce a 64-bit “row hash”: a 1 bit means the pixel intensity is increasing in the x direction, 0 means it’s decreasing

4.  Do the same to produce a 64-bit “column hash” in the y direction

5.  Combine the two values to produce the final 128-bit hash value

##### Implementation

ImageHash 4.0 <https://pypi.org/project/ImageHash/>

##### Results

Results given by the ImageHash implementation of D-hash algorithm does not provides reliable results, but better than a-hash results.

<span>0.39</span> <img src="sota-ressources/outputs-evaluation/d-hash/bestthana.png" title="fig:" alt="d-hash" />

<span>0.60</span> <img src="sota-ressources/outputs-evaluation/d-hash/bestthana_2.png" title="fig:" alt="d-hash" />

<span>0.3</span> <img src="sota-ressources/outputs-evaluation/d-hash/echec.png" title="fig:" alt="d-hash" />

<span>0.66</span> <img src="sota-ressources/outputs-evaluation/d-hash/echec_2.png" title="fig:" alt="d-hash" />

###### Time

nobs : 207s min time : 0.00211s max time : 0.00379s mean :0.0024236169990134123s variance : 1.3200716728248016e-07s skewness : 2.412448208288436s kurtosis : 5.039791588290182

###### “Vertical” variation

A variation of the d-hash algorithm is available, as d-hash vertical.

<span>0.42</span> <img src="sota-ressources/outputs-evaluation/d-hash-vertical/interesting_mismatch.png" title="fig:" alt="Vertical d-hash" />

<span>0.56</span> <img src="sota-ressources/outputs-evaluation/d-hash-vertical/interesting_mismatch_2.png" title="fig:" alt="Vertical d-hash" />

### P-HASH - Perceptual Hash

From ... \[40\] and \[18\] and \[42\]
Exist in mean and median flavors
8 bits for a image vector.
Java implementation : \[41\]

##### Pro

-   Robustness to gamma

-   Robustness to color histogram adjustments

-   Should be robust to rotation, skew, contrast adjustment and different compression/formats.

-   , C++, API

##### Steps of the algorithm

1.  Reduce size of the input image to 32x32 (needed to simplify DCT computation)

2.  Reduce color to grayscale (same)

3.  Compute the DCT : convert image in frequencies, a bit similar to JPEG compression

4.  Reduce the DCT : keep the top-left 8x8 of the DCT, which are the lowest frequencies

5.  Compute the average DCT value : without the first term (i.e. solid colors)

6.  Further reduce the DCT : Set the 64 hash bits to 0 or 1 depending on whether each of the 64 DCT values is above or below the average value.

7.  Construct the hash : create a 64 bits integer from the hash

8.  Comparing with Hamming Distance (threeshold = 21)

##### Implementation

ImageHash 4.0 <https://pypi.org/project/ImageHash/>

##### Results

Still some strange results

<span>0.52</span> <img src="sota-ressources/outputs-evaluation/p-hash/strange_0.png" title="fig:" alt="P-hash" />

<span>0.47</span> <img src="sota-ressources/outputs-evaluation/p-hash/strange_1.png" title="fig:" alt="P-hash" />

###### Time

nobs : 207 min time : 0.00253s max time : 0.63245s mean :0.009314882582512455s variance : 0.0020187846451833486s skewness : 13.117889676404076s kurtosis : 177.8720654998952

###### “Simple” variation

A variation of the p-hash algorithm is available, as p-hash simple.

<span>0.55</span> <img src="sota-ressources/outputs-evaluation/p-hash-simple/error_0.png" title="fig:" alt="P-hash - Simple" />

<span>0.44</span> <img src="sota-ressources/outputs-evaluation/p-hash-simple/good_black.png" title="fig:" alt="P-hash - Simple" />

### W-HASH - Wavelet Hash

From ... Uses DWT instead of DCT. \[TO LOOK\]

##### Implementation

ImageHash 4.0 <https://pypi.org/project/ImageHash/>

##### Results

Better than others, but still some strange/wrong results.

<span>0.55</span> <img src="sota-ressources/outputs-evaluation/w-hash/strange_0.png" title="fig:" alt="W-hash" />

<span>0.44</span> <img src="sota-ressources/outputs-evaluation/w-hash/error_0.png" title="fig:" alt="W-hash" />

<span>0.8</span> <img src="sota-ressources/outputs-evaluation/w-hash/error_1.png" title="fig:" alt="W-hash" />

###### Time

nobs : 207 min time : 0.00214s max time : 0.53841s mean :0.00532086229554697s variance : 0.0013867749582104625s skewness : 14.274196161282449s kurtosis : 201.83699346303464

### SimHash - Charikar’s simhash

From ... \[23\]
repository of 8B webpages, 64-bit simhash fingerprints and k = 3 are reasonable.
C++ Implementation

### R-HASH

From ... \[40\]

Equivalent to A-Hash with more granularity of masks and transformation. Ability to apply “masks” (color channel, ignoring (f.ex. the lowest two) bits of some/all values) and “transformations” at comparison time. (color channel swaps)

48 bits for a rgb image vector

##### Pro

-   Masks and transformation available

-   More precise masks (than A-hash)

-   More precise transformations (than A-hash)

##### Con

-   Larger memory footprint

##### Steps of the algorithm

1.  Image scaled to 4x4

2.  Compute vector

3.  Comparison = sum of absolute differences: abs(a\[0\]-b\[0\]) + abs(a\[1\]-b\[1\]) + ... + abs(a\[47\]-b\[47\]) = 48 dimensional manhattan distance

### Spectral-HASH

From \[54\]. A word is given in \[40\]

The bits are calculated by thresholding a subset of eigenvectors of the Laplacian of the similarity graph

Similar performance to RBM

![Spectral Hashing comparison from \[54\] <span data-label="fig:spectral_hashing_comparison"></span>](sota-ressources/spectral_hashing_comparison.png)

### LSH - Locality Sensitve Hashing

Same as E2LSH ? Chooses random projections so that two closest image samples in the feature space fall into the same bucket with a high probability, from \[9\]

### E2LSH - LSH - Locality Sensitve Hashing

From \[15\] a word is given in \[54\] and \[9\].
The code is calculated by a random linear projection followed by a random threshold, then the Hamming distance between codewords will asymptotically approach the Euclidean distance between the items.

Not so far from Machine Learning Approaches, but outperformed by them.

##### Pro

-   Faster than Kdtree

##### Con

-   Very inefficient codes (512 bits for a picture (TO CHECK))

### Nilsimsa hash - Locality sensitive hash

A word in \[27\]

##### Pro

-   Open Source

### TLSH - Trend Micro Locality Sensitive Hashing

From \[27\] directly performed on file, not only pictures. Therefore, running TLSH on PNG can’t provide consistent results, as the structure of the file is taken into account (and so it’s meaningless compression). Files have to be uncompressed (e.g. some types of BMP files) to have consistent resuls with TLSH.

##### Pro

-   Parametered threeshold (below 30 in original paper)

-   Open Source

###### Time

Normal version : nobs : 207s min time : 0.00083s max time : 0.00165s mean :0.00095s variance : 0.0s skewness : 2.7512s kurtosis : 7.24537 No-length version : nobs : 207s min time : 0.00095s max time : 0.00455s mean :0.00115s variance : 0.0s skewness : 7.60762s kurtosis : 67.0044

<span>0.59</span> <img src="sota-ressources/outputs-evaluation/tlsh/example_0.png" title="fig:" alt="TLSH (normal) with PNG" />

<span>0.40</span> <img src="sota-ressources/outputs-evaluation/tlsh/clean_match.png" title="fig:" alt="TLSH (normal) with PNG" />

<span>0.51</span> <img src="sota-ressources/outputs-evaluation/tlsh/mismatch_0.png" title="fig:" alt="TLSH (normal) with PNG" />

<span>0.48</span> <img src="sota-ressources/outputs-evaluation/tlsh/strange_results.png" title="fig:" alt="TLSH (normal) with PNG" />

<span>0.49</span> <img src="sota-ressources/outputs-evaluation/tlsh_nolength/strange_distance.png" title="fig:" alt="Inconsistent distance regarding pictures - TLSH (no length) with PNG" />

<span>0.50</span> <img src="sota-ressources/outputs-evaluation/tlsh_nolength/strange_distance_2.png" title="fig:" alt="Inconsistent distance regarding pictures - TLSH (no length) with PNG" />

### SSDeep - Similarity Digest 

From ... few words on it in \[31\]

Implementation (C) at \[50\]

Historically the first fuzzing algorithm. CTPH type.

![ Hashing time from \[20\] <span data-label="fig:ssdeep_timing"></span>](sota-ressources/ssdeep_time.png)

##### Pro

-   Effective for text (Spam, ..)

-   Open Source

##### Con

-   Not effective for Images, Videos, ...

-   Les effective than Sdhash

##### Steps of the algorithm

1.  Rolling hashing to split document into “6 bits values segments”

2.  Uses hash function (MD5, SHA1, ..) to produce a hash of each segment

3.  Concatenate all hashes to create the signature (= the fuzzy hash)

### SDHash - Similarity Digest Hash

From ... Roussev in 2010 few words on it in \[31\]

Uses Bloom Filters to identify similarities between files on condition with common features. (Quite blurry)

##### Pro

-   More accurate than VHash, SSDeep, MRSHV2

-   Options available (TO CHECK) - See a particular implementation used in \[31\]

-   Open Source

##### Con

-   Slow compared to MVHash, SSDeep, MRSHV2

##### Steps of the algorithm

1.  Perform a hash/entropy (TO CHECK) calculation with a moving window of 64 bits.

2.  Features (? How are they recognized?) are hashed with SHA-1

3.  Features are inserted into a Bloom Filter

### MVHash - Majority Vote Hash

From ... few words on it in \[31\]

It is Similarity Preserving Digest (SPD) Uses Bloom Filters

##### Pro

-   almost as fast as SHA-1 (paper)

##### Steps of the algorithm

1.  Majority vote on bit level (transformation to 0s or 1s)

2.  RLE = Run Length Encoding, represents 0s and 1s by their length

3.  Create the similarity digest (? TO CHECK)

### MRSH V2 - MultiResolution Similarity Hashing

From ... few words on it in \[31\] Variation of SSDeep, with polynomial hash instead of rolling hash (djb2)

##### Pro

-   Fast than SDHash

##### Con

-   Slow compared to MVHash, SSDeep

### GIST - 

From \[26\] a word in \[21\]

Holistic feature which is based on a low dimensional representation of the scene that does not require any form of segmentation, and it includes a set of perceptual dimensions (naturalness, openness, roughness, expansion, ruggedness)

Per subregion features
----------------------

**Per subregion** Example : Histogram of Oriented Gradients (HOG)

Holistic feature ...

### HOG - Histogram of Oriented Gradients

From ... A word in \[37\] The idea is to describe shape information by gradient orientation in localized sub-regions.

Algorithms combination
======================

Few sources expose algorithms combination for specific goals. e.g. \[4\], \[58\], \[49\]

Phishing
--------

Classification of approaches :

-   Non-content based methods : URL, whois, ..

-   Content-based methods : text, images, HTML, js, css, ...
    Sensitive to image injection instead of DOM, of invisible characters, ...

-   Visual similarity and image processing methods

-   Hybrid methods

“scale and rotation invariance \[...\] are rarely seen in phishing pages because the pages must be very similar to the corresponding authentic pages to deceive unsuspecting users. ” \[10\]

### Visual similarity - Histogramm

“Web pages \[...\] usually contain fewer colors than paintings or photographs \[and\] have similar color distributions” from \[10\]. They also state that add banners add a high amount of “color histogram” noise.

### Visual similarity - Hash

### Visual similarity - Keypoints

\[10\] is presenting keypoints based phshing website detection named L-CCH. L-CCH uses Harris-Laplacian corners detection on gray scale pictures, and store keypoint as Contrast Context Histograms. They also highlight “to judge two Web pages’similarity, we must consider \[keypoints\] spatial distribution, or locations.”. Then, they also cluster keypoints in areas, and perform area matching. Each cluster of keypoints is evaluated to each candidate cluster of keypoints. Their solution seems not to handle rotation and scaling variation.

<img src="sota-ressources/LCCH_idea.png" alt="L-CCH results : Harris based + Clustering [10]" />

<img src="sota-ressources/LCCH_results.png" alt="L-CCH results : Harris based + Clustering [10]" />

\[<span class="citeproc-not-found" data-reference-id="chenDetectingVisuallySimilar2010a">**???**</span>\] is merging structures and layout to “higher level” structures before perform matching. They report %95 true positive rate with less than %1.7 false positive

\[1\] uses a two passes method, based on metadata (SSL, URL, .. 49% to 66.78% detection rate) and then SIFT keypoint matching. It reported %90 of accuracy with less than %0.5 of false positives.

\[39\] uses a spatial postprocessing algorithm upon SIFT, to remove matches that are not relevant, if not “spatially consistent” with source picture. \[38\] seems to use a similar idea.

### Visual similarity - Text handling

Non-Specific
------------

### Block-based approach + KeyPoint approach for Image manipulation

From \[28\]

Local Features Algorithms
=========================

Goal is to transform visual information into vector space

Comparison overview
-------------------

![Benchmarking of SIFT, SURF, ORB, AKAZE with RATIO and GMS selection ; FLANN or Hamming for distance. SP curves show the success ratio or success number (number of correspondance for AP) with thresholds. X-Axis being the threeshold. AP curves illustrate the mean number of verified correspondences with thresholds.\[<span class="citeproc-not-found" data-reference-id="bianImageMatchingApplicationorienteda">**???**</span>\] <span data-label="fig:benchmarking1"></span>](sota-ressources/benchmarking_1.png)

![Benchmarking of SIFT, SURF, ORB, AKAZE, BRISK, KAZE with computation time. Ordered best time from best to worst : red, green, blue, black. \[<span class="citeproc-not-found" data-reference-id="bianImageMatchingApplicationorienteda">**???**</span>\] <span data-label="fig:benchmarking2"></span>](sota-ressources/benchmarking_2.png)

![Benchmarking of SIFT, SURF, ORB, AKAZE, BRISK, KAZE on robustness (RS), accuracy (AS), sufficiency (SS). Ordered best time from best to worst : red, green, blue, black. \[<span class="citeproc-not-found" data-reference-id="bianImageMatchingApplicationorienteda">**???**</span>\] <span data-label="fig:benchmarking3"></span>](sota-ressources/benchmarking_3.png)

In few words :

-   **Robustness**
    Success ratio (15difference max from real position) = Succes to match pairs
    Non-binary are better than binaries algorithms. Number of interest points change the best matching method to choose.

-   **Accuracy**
    Success ratio (5difference max from real position) = Are pairs are matched “for sure”
    Non-binary are better than binaries algorithms

-   **Sufficiency**
    Mean number of correctly geometric matched pairs.
    ORB-GMS is the best.

-   **Efficiency**
    Feature detection time + Feature matching time.
    ORB and BRISK are the fastest, KASE the slowest.

Some more comparisons are performed in \[44\] about robustness of different algorithms.

<span>0.49</span> <img src="sota-ressources/repetability_blurring.png" title="fig:" alt="Robustness (nb of matches/nb points in original image in %) comparison from [44]" />

<span>0.49</span> <img src="sota-ressources/repetability_brightness.png" title="fig:" alt="Robustness (nb of matches/nb points in original image in %) comparison from [44]" />

<span>0.49</span> <img src="sota-ressources/repetability_rotation.png" title="fig:" alt="Robustness (nb of matches/nb points in original image in %) comparison from [44]" />

<span>0.49</span> <img src="sota-ressources/repetability_scaling.png" title="fig:" alt="Robustness (nb of matches/nb points in original image in %) comparison from [44]" />

A large performance overview has been operated by \[35\]. Many information are extracted from their tests and are showed on each algorithm description.The paper is ordering algorithms thanks to different objective.

**Ability to detect high quantity of features** :
*O**R**B* &gt; *B**R**I**S**K* &gt; *S**U**R**F* &gt; *S**I**F**T* &gt; *A**K**A**Z**E* &gt; *K**A**Z**E*

**Computational efficiency of feature-detection-description per feature-point :**
*O**R**B* &gt; *O**R**B*(1000)&gt;*B**R**I**S**K* &gt; *B**R**I**S**K*(1000)&gt;*S**U**R**F*(64*D*)&gt;*S**U**R**F*(128*D*)&gt;*A**K**A**Z**E* &gt; *S**I**F**T* &gt; *K**A**Z**E*

**Efficient feature-matching per feature-point :**
*O**R**B*(1000)&gt;*B**R**I**S**K*(1000)&gt;*A**K**A**Z**E* &gt; *K**A**Z**E* &gt; *S**U**R**F*(64*D*)&gt;*O**R**B* &gt; *B**R**I**S**K* &gt; *S**I**F**T* &gt; *S**U**R**F*(128*D*)

**Speed of total image matching :**
*O**R**B*(1000)&gt;*B**R**I**S**K*(1000)&gt;*A**K**A**Z**E* &gt; *K**A**Z**E* &gt; *S**U**R**F*(64*D*)&gt;*S**I**F**T* &gt; *O**R**B* &gt; *B**R**I**S**K* &gt; *S**U**R**F*(128*D*)

![Results from \[35\] - Time cost - mean value on original paper dataset<span data-label="fig:tests"></span>](sota-ressources/performance_algo.png)

<img src="sota-ressources/comparison_graph_0.png" alt="Results from [35] - Resilience to changes graphs" />

Non-binary features
-------------------

### SIFT- Scale Invariant Feature Transform

From the original paper \[22\] and a concise explanation from \[45\] 3x less fast than Harris Detector

SIFT detects scale-invariant key points by finding local extrema in the difference-of-Gaussian (DoG) space. \[21\]
Each key point is described by a 128-dimensional gradient orientation histogram. Subsequently, all SIFT descriptors are modeled/quantized using a bag-of-words (BoW). The feature vector of each image is computed by counting the frequency of the generated visual words in the image.

Interesting “usability” notices are presented in \[34\], as skiping first octave features, ...

#### Pro

-   “SIFT is \[...\] most accurate feature-detector descriptor for scale, rotation and affine variations (overall).” \[35\]

#### Con

-   and not included in OpenCV (only non-free module)

-   Slow : “a general perception that SURF is computationally efficient than SIFT, but the experiments revealed that SURF(128D) algorithm takes more time than SIFT(128D)” \[35\]

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

### SIFT-FLOW

From \[14\], realize in motion prediction from a single image, motion synthesis via object transfer and face recognition.

##### Implementation

SIFT Flow (modified version of SIFT) C++ \[59\] at <http://people.csail.mit.edu/celiu/SIFTflow/>

### Root-SIFT

From \[3\]
Better performances as SIFT, but no implementation found.

### SURF – Speeded-Up Robust Features

\[5\] Use the BoWs to generate local features.

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

### U-SURF – Upright-SURF

Rotation invariance can be “desactivated” for faster results, by bypassing the main orientation finding, and is robust up to 15rotation.

### GSSIS - Generalized Scale-Space Interest Points

From \[47\], generalized interest point, with colors exension, of SIFT and SURF.

Roughly : uses more complicated way of generating local interest points.

#### Pro

-   Scale-invariant

### LBP - Local Binary Pattern

From \[21\], use the BoWs to generate local features

Binary features
---------------

### ORB – Oriented FAST and Rotated BRIEF

From \[30\] which is rougly a fusion of FAST and BRIEF. See also \[46\] The threeshold of 0.75 (Lowe ratio) should be modified for ORB. 0.89 seems to be the equivalent to 0.75

#### Pro

-   Not patented

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

###### Option explanation

Mostly from \[48\], \[60\] :
To be clear :

-   **Target picture** = request picture = new picture = picture we want to find correlation on

-   **Candidate picture** = stored picture = old pictures = pictures already parsed, prepared and stored, to find correlation on.

Perform a feature matching :

-   **Brute-Force matcher**, with bf.match(), is simple. It takes the descriptor of one feature of the target picture and is evaluated with all other features of all candidate pictures, using some distance calculation. The closest one is returned. It returns a list of matches. Use crossCheck=True.

-   **KnnMatch**, with bf.knnMatch(), returns for each descriptor of the target picture, the n-best matches with descriptors of a candidate picture. It searches for N-best candidate for each descriptor. It returns list of a list of matches. Use crossCheck=False and then do the ratio test.

Remove outliers and bad matches :

-   **CrossCheck** is an alternative to the ratio test. Cross-check does matching of two sets of descriptors D1 and D2 in both directions (D1 to D2 and D2 to D1) retaining matches that exists in both.

-   A **ratio test** can be performed on each k-uplets. Repetitive patterns are detected if the distance between one descriptor of the target picture is the same with the two best descriptors of the candidate picture. 2 points on the candidate picture matched 1 point on the target picture.

**RANSAC** filter matches. (TO CHECK)

Print nice graphs :

-   **cv2.drawKeypoints()** to draw keypoints

-   **cv2.drawMatches()** helps us to draw the matches. It stacks two images horizontally and draw lines from first image to second image showing best matches.

-   **cv2.drawMatchesKnn** draws all the k best matches. If k=2, it will draw two match-lines for each keypoint.

###### Analysis

Distance can be computed in many ways. Here is an analysis of each of the used distances.

-   Min length : the number of matches divided by the minimal number of descriptors of both pictures.
    This doesn’t work well, because if one of both pictures has a low number of descriptors, it will act as an “attractor” : this picture will be the closest one of many other one. It does not use the “internal distance of a match” : the distance of one descriptor to the other.

-   Max length : the number of matches divided by the minimal number of descriptors of both pictures.
    This works pretty well, removing the issue encountered by the min length. However it does not use the “internal distance of a match” : the distance of one descriptor to the other.

-   Mean of matches : it makes use of the “internal distance of a match” : the distance of one descriptor to the other. The distance between two pictures is computed as the mean of the matches distance. This doesn’t work well, for the same reason as min-length : if one of both pictures has a low number of descriptors, it will act as an “attractor” : this picture will have very few matches with others, but this small set of matches will have very “good distances”. .

###### Time

MIN-version : nobs : 207 min time : 0.00022s max time : 1.22806s mean :0.78938s variance : 0.06399s skewness : -2.6371s kurtosis : 5.44295
MAX-version : nobs : 207 min time : 0.00022s max time : 1.89294s mean :0.81612s variance : 0.0911s skewness : -1.02273s kurtosis : 3.77603
RATIO-version : nobs : 207 min time : 0.00022s max time : 2.25978s mean :0.92306s variance : 0.14716s skewness : -0.13801s kurtosis : 2.98186
BF + STD + LENMAX (with picture saving): nobs : 191 min time : 0.00018s max time : 18.99671s mean :2.99756s variance : 5.26731s skewness : 3.88639s kurtosis : 23.2982
CONFIGURATION : RATIO TEST KNN 2 False FLANN LSH nobs : 191 min time : 0.51244s max time : 17.48676s mean :2.42647s variance : 4.23831s skewness : 4.51153s kurtosis : 24.8294

<span>0.58</span> <img src="sota-ressources/outputs-evaluation/orb_min/microsoft_match.png" title="fig:" alt="Results - ORB - min version" />

<span>0.43</span> <img src="sota-ressources/outputs-evaluation/orb_min/attractor_problem_min.png" title="fig:" alt="Results - ORB - min version" />

<span>0.6</span> <img src="sota-ressources/outputs-evaluation/orb_min/how_handle_no_descriptors.png" title="fig:" alt="Results - ORB - min version" />

<span>0.51</span> <img src="sota-ressources/outputs-evaluation/orb_max/KBC_perfect_match.png" title="fig:" alt="Results - ORB - max version" />

<span>0.48</span> <img src="sota-ressources/outputs-evaluation/orb_max/Microsoft_good_match_threeshold.png" title="fig:" alt="Results - ORB - max version" />

<span>0.8</span> <img src="sota-ressources/outputs-evaluation/orb_max/swedish_bank_good_match.png" title="fig:" alt="Results - ORB - max version" />

<span>0.51</span> <img src="sota-ressources/outputs-evaluation/orb_max/KBC_perfect_match.png" title="fig:" alt="Results - ORB - max version" />

<span>0.48</span> <img src="sota-ressources/outputs-evaluation/orb_max/Microsoft_good_match_threeshold.png" title="fig:" alt="Results - ORB - max version" />

<span>0.8</span> <img src="sota-ressources/outputs-evaluation/orb_max/swedish_bank_good_match.png" title="fig:" alt="Results - ORB - max version" />

Following pictures are showing drawbacks of ORB algorithm. As a first “general overview” of some matching results, few examples with commentary are giv en below. Tests were performed in “ratio” configuration, however, drawbacks are generalized to other submethods.
Few tips to analyze following pictures :

-   **Parrallel lines** (if there is not rotation) are a indicator of quality matching. It keeps the spatial consistency between source and candidate pictures.

-   **Text** seems to be a problem. Letters are matched to letters, generating false positive. It also “uses” descriptor space (number of descriptors is artificially limited), and so, hinders true logo (for example) to be described and used.

<span>0.58</span> <img src="sota-ressources/outputs-evaluation/orb_matches/batchtextmatching.png" title="fig:" alt="Results - ORB - drawbacks examples 1/3" />

<span>0.37</span> <img src="sota-ressources/outputs-evaluation/orb_matches/cleargoodfirstmatch.png" title="fig:" alt="Results - ORB - drawbacks examples 1/3" />

<span>0.4</span> <img src="sota-ressources/outputs-evaluation/orb_matches/EdgeCase_shoulditmatch.png" title="fig:" alt="Results - ORB - drawbacks examples 1/3" />

<span>0.59</span> <img src="sota-ressources/outputs-evaluation/orb_matches/good_match_text.png" title="fig:" alt="Results - ORB - drawbacks examples 1/3" />

<span>0.49</span> <img src="sota-ressources/outputs-evaluation/orb_matches/good_microsoft_parrallel.png" title="fig:" alt="Results - ORB - drawbacks examples 2/3" />

<span>0.50</span> <img src="sota-ressources/outputs-evaluation/orb_matches/not_best_matching_due_to_text.png" title="fig:" alt="Results - ORB - drawbacks examples 2/3" />

<span>1</span> <img src="sota-ressources/outputs-evaluation/orb_matches/GoodTypoSpecificImage.png" title="fig:" alt="Results - ORB - drawbacks examples 2/3" />

<span>1</span> <img src="sota-ressources/outputs-evaluation/orb_matches/perfect_microsoft_match.png" title="fig:" alt="Results - ORB - drawbacks examples 2/3" />

<span>1</span> <img src="sota-ressources/outputs-evaluation/orb_matches/text_problem.png" title="fig:" alt="Results - ORB - drawbacks examples 3/3" />

<span>1</span> <img src="sota-ressources/outputs-evaluation/orb_matches/text_problem_2.png" title="fig:" alt="Results - ORB - drawbacks examples 3/3" />

<span>0.5</span> <img src="sota-ressources/outputs-evaluation/orb_matches/text_problem_long_3.png" title="fig:" alt="Results - ORB - drawbacks examples 3/3" />

<span>0.48</span> <img src="sota-ressources/outputs-evaluation/orb_matches/whitepagetextproblem.png" title="fig:" alt="Results - ORB - drawbacks examples 3/3" />

### BRISK - 

### AKASE - 

Unsorted
--------

### PSO

From ... few words in \[25\]

### SKF

From \[25\]

Faster than PSO.

### RPM - Robust Point Matching

From ... Few words in \[36\] Unidirectional matching approach. Does not “check back” if a matching is correct. Seems to achieve only the transformation (geometry matching) part.

### BRIEF – Binary Robust Independent Elementary Features

Extract binary strings equivalent to a descriptor without having to create a descriptor

See BRIEF \[61\]

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

### R-BRIEF – Rotation (?) BRIEF

Variance and mean of a bit-feature (bitstring) is lost if the direction of keypoint is aligned (TO VERIFY : would this mean that there is a preferential direction in the pair of point selection ? )

Uncorrelated tests (TO CHECK WHAT IT IS) are selected to ensure a high variance.

### CenSurE

### KASE - 

Shipped in OpenCV library. Example can be found at \[24\]

#### Steps of the algorithm

1.  Extrema detection

2.  Keypoint localization and filtering

3.  Orientation assignement

4.  Keypoint descriptors

5.  Keypoint Matching

### Delaunay Graph Matching

Algorithm from 2012, quite advanced. Would need some tests or/and review See M1NN \[13\] that is presenting 3 algorithms :

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

### Fast Spectral Ranking

From \[19\] Seems to have quite fast result, ranking algorithm. Still dark areas over the explanations.

### GHM - Generalized Hierarchical Matching Framework

From \[11\] Roughly, the algorithm split the input picture into interest areas, and then do matching on these different areas.

This tries to achieve a object-oriented recognition. It uses Saliency Map.

This (TO CHECK) is a non-rectangle version of SPM.

![Hierarchical Hashing as showed in \[11\] <span data-label="fig:generalized-matching"></span>](sota-ressources/hierarchical-matching.png)

#### Steps of the algorithm

1.  Multiple scale detection is performed in each image and the obtained multi-scale scores are averaged to get final single object confidence map.

Neural networks – Black box algorithms
======================================

See \[21\] to get a larger overview of deeplearning capabilities, applied to a particular field.

FAST – Features from Accelerated Segment Test
---------------------------------------------

From \[43\] the algorithm is mainly Machine Learning, but as far as I can see, there is no direct need of machine learning in the algorithm, but for speed.

It seems that the selection of candidate pixel, and the selection of a threeshold is holded by Machine Learning. It also seems, that “mostly brighter”, “similar” and “mostly darker” pixels are used to feed a decision tree (ID3 algorithm - decision tree classifier) to allow a fast recognition of a corner.

![Corner detector from \[29\] <span data-label="fig:spectral_hashing_comparison"></span>](sota-ressources/corner-detector.png)

#### Pro

-   “High performance” (HOW MUCH, TO CHECK)

#### Con

-   “Too” sensitive if n&lt;12 : increase in false-positive

-   Many calculation just to “throw away” a pixel.

-   Many True-postive around the same position

-   Not robust to high levels of noise

-   Dependant on a threshold

#### Steps of the algorithm

1.  Extrema detection For each pixel, select a cicle-patch (not disk-patch, not a surface!) of 16 pixels around it. The pixel is a corner if there is n (n=12) contiguous pixels parts of the circle, which are all brighter or all darker than the center-pixel.

    It’s easy to remove all “not-corner” points, by checking only few (1, 9, 5 and 13) pixels of the circle.

2.  Keypoint localization and filtering

3.  Orientation assignement

4.  Keypoint descriptors

5.  Keypoint Matching

CNN - Convolutional Neural Network
----------------------------------

From ... \[15\]

FRCNN - Faster RCNN
-------------------

From ... \[33\] Mainly for faces detection.

#### Pro

-   M

RTSVMs - Robust Transductive Support Vector Machines
----------------------------------------------------

From \[15\] Seems to scale very well (&gt;1 Million data)

Uses a hashing method, binary hierarchical trees and TSVM classifier.

![Biary hierarchical tree from \[15\] <span data-label="fig:spectral_hashing_comparison"></span>](sota-ressources/rtsvms.png)

RBM - Restricted Boltzmann machine
----------------------------------

From ... A word is given in \[54\]

To learn 32 bits, the middle layer of the autoencoder has 32 hidden units Neighborhood Components Analysis (NCA) objective function = refine the weights in the network to preserve the neighborhood structure of the input space.

#### Pro

-   More compact outputs code of picture than E2LSH = Better performances

RPA - Robust Projection Algorith
--------------------------------

From ... \[18\]

Boosting SSC
------------

From ... A word is given in \[54\]

#### Pro

-   Better than E2LSH

#### Con

-   Worst than RBM

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

Utility algorithms
==================

SWS - Sliding Windows Search
----------------------------

From ... \[37\] A bounding box is sliding on the picture, and an objet-existence score in the bounding box is computed for each position, and each rectangle size.

#### Pro

-   B

#### Con

-   Too complex ! *O*(*N*<sup>4</sup>) windows to evaluate, with N = resolution on one axis of the picture

Heuristics can be used to reduce the expected complexity of the algorithm. The picture is reduced in size, with a constant size bounding box, to find objects at different scales. These heuristics may miss objects.

ESS - Efficient Subwindow Search
--------------------------------

From \[37\] Based on a branch-and-bound algorithm. The algorithm does not evaluate all subrectangle of rectangle with a low evaluation of the best chance they have to contain an object.

#### Pro

-   Sublinear to number of pixels. ( below *O*(*N*) )

SLICO - Simple Linear Iterative Clustering
------------------------------------------

Cluster a picture into smaller chunks. For example, used in \[28\] for Copy Move detection.

HSNW - ... indexing
-------------------

From ... A word in \[12\]

Raw results
-----------

### Phishing dataset / Hashing based

| Conf               | nobs | min time | max time | mean    | variance | skewness | kurtosis | Quality |
|:-------------------|:-----|:---------|:---------|:--------|:---------|:---------|:---------|:--------|
| TLSH PNG           | 207  | 0.00079  | 0.00121  | 0.0009  | 0.0      | 3.65389  | 18.2277  | 0.42512 |
| TLSH BMP           | 207  | 0.00076  | 0.00128  | 0.00082 | 0.0      | 5.54139  | 37.84432 | 0.58937 |
| AHASH PNG          | 207  | 0.00196  | 0.00438  | 0.00217 | 0.0      | 2.91552  | 8.59409  | 0.57971 |
| AHASH BMP          | 207  | 0.002    | 0.00422  | 0.00225 | 0.0      | 2.71252  | 8.48601  | 0.57971 |
| PHASH PNG          | 207  | 0.00193  | 0.00372  | 0.00213 | 0.0      | 2.99038  | 8.84388  | 0.56039 |
| PHASH BMP          | 207  | 0.00197  | 0.00439  | 0.00233 | 0.0      | 1.89519  | 3.85316  | 0.55072 |
| PHASH SIMPLE PNG   | 207  | 0.00195  | 0.00383  | 0.00212 | 0.0      | 3.91599  | 16.23136 | 0.52657 |
| PHASH SIMPLE BMP   | 207  | 0.00197  | 0.00432  | 0.00228 | 0.0      | 2.41582  | 6.46488  | 0.52174 |
| DHASH PNG          | 207  | 0.002    | 0.00351  | 0.0022  | 0.0      | 2.63954  | 6.74112  | 0.60386 |
| DHASH BMP          | 207  | 0.00199  | 0.00391  | 0.00216 | 0.0      | 5.05627  | 27.72867 | 0.60386 |
| DHASH VERTICAL PNG | 207  | 0.00195  | 0.00392  | 0.00227 | 0.0      | 2.27337  | 4.40377  | 0.57488 |
| DHASH VERTICAL BMP | 207  | 0.00201  | 0.00346  | 0.00211 | 0.0      | 5.95159  | 44.91675 | 0.56522 |
| WHASH PNG          | 207  | 0.002    | 0.00565  | 0.00231 | 0.0      | 3.74684  | 12.5523  | 0.53623 |
| WHASH BMP          | 207  | 0.0019   | 0.00339  | 0.002   | 0.0      | 6.61575  | 51.99721 | 0.54106 |

### Phishing dataset / Feature based

Note : nobs is lower than hash base algorithm, due to removal of None-feature pictures.

| Conf                    | nobs | min time | max time | mean     | variance | skewness  | kurtosis | True Positive |
|:------------------------|:-----|:---------|:---------|:---------|:---------|:----------|:---------|:--------------|
| ORB                     |      |          |          |          |          |           |          |               |
| LEN MAX - KNN 2         |      |          |          |          |          |           |          |               |
| Crosscheck : False      |      |          |          |          |          |           |          |               |
| FLANN LSH               |      |          |          |          |          |           |          |               |
| FAR THREESHOLD          | 190  | 0.26489s | 1.57223s | 1.11384s | 0.04294s | -0.97579s | 1.09073  | 0.63158       |
| ORB                     |      |          |          |          |          |           |          |               |
| LEN MAX - KNN 2         |      |          |          |          |          |           |          |               |
| Crosscheck : False      |      |          |          |          |          |           |          |               |
| FLANN LSH               |      |          |          |          |          |           |          |               |
| RATIO CORRECT           | 190  | 0.37287s | 2.18801s | 1.19707s | 0.08682s | 0.4874s   | 0.84502  | 0.62105       |
| ORB                     |      |          |          |          |          |           |          |               |
| LEN MAX - STD           |      |          |          |          |          |           |          |               |
| Crosscheck : True       |      |          |          |          |          |           |          |               |
| BF                      |      |          |          |          |          |           |          |               |
| NO FILTER               | 190  | 0.14815s | 2.71545s | 1.76562s | 0.05727s | -1.95637s | 18.60976 | 0.65263       |
| ORB (1000) PNG          |      |          |          |          |          |           |          |               |
| LEN MAX - STD           |      |          |          |          |          |           |          |               |
| Crosscheck : True       |      |          |          |          |          |           |          |               |
| BF                      |      |          |          |          |          |           |          |               |
| NO FILTER               | 190  | 0.39845  | 27.05392 | 7.55308  | 5.26437  | 3.50726   | 27.80995 | 0.63684       |
| ORB(100) PNG            |      |          |          |          |          |           |          |               |
| LEN MAX - STD           |      |          |          |          |          |           |          |               |
| Crosscheck : True       |      |          |          |          |          |           |          |               |
| BF                      |      |          |          |          |          |           |          |               |
| NO FILTER               | 190  | 0.05959  | 0.70835  | 0.20155  | 0.01367  | 1.01663   | 1.39958  | 0.59474       |
| ORB(300) PNG            |      |          |          |          |          |           |          |               |
| LEN MAX - STD           |      |          |          |          |          |           |          |               |
| Crosscheck : True       |      |          |          |          |          |           |          |               |
| BF                      |      |          |          |          |          |           |          |               |
| NO FILTER               | 190  | 0.08     | 1.20131  | 0.68654  | 0.01096  | -0.37938  | 10.68281 | 0.61579       |
| ORB BMP (read problem?) |      |          |          |          |          |           |          |               |
| MEAN DIST PER PAIR      |      |          |          |          |          |           |          |               |
| STD                     |      |          |          |          |          |           |          |               |
| Crosscheck : True       |      |          |          |          |          |           |          |               |
| BF                      |      |          |          |          |          |           |          |               |
| NO FILTER               | 190  | 0.13807  | 1.97816  | 1.6771   | 0.02955  | -6.69731  | 53.39513 | 0.56842       |
| ORB BMP (read problem?) |      |          |          |          |          |           |          |               |
| MEAN DIST PER PAIR      |      |          |          |          |          |           |          |               |
| KNN 2                   |      |          |          |          |          |           |          |               |
| Crosscheck: False       |      |          |          |          |          |           |          |               |
| FLANN LSH               |      |          |          |          |          |           |          |               |
| RATIO CORRECT           | 190  | 0.30946  | 2.64872  | 1.21666  | 0.08734  | 0.73779   | 3.23452  | 0.39474       |
| ORB BMP (read problem?) |      |          |          |          |          |           |          |               |
| MEAN DIST PER PAIR      |      |          |          |          |          |           |          |               |
| KNN 2                   |      |          |          |          |          |           |          |               |
| Crosscheck: False       |      |          |          |          |          |           |          |               |
| FLANN LSH               |      |          |          |          |          |           |          |               |
| FAR THREESHOLD          | 190  | 0.27585  | 1.53042  | 1.09527  | 0.0407   | -1.11117  | 1.12641  | 0.34211       |
| ORB PNG                 |      |          |          |          |          |           |          |               |
| MEAN DIST PER PAIR      |      |          |          |          |          |           |          |               |
| KNN 2                   |      |          |          |          |          |           |          |               |
| Crosscheck : False      |      |          |          |          |          |           |          |               |
| FLANN LSH               |      |          |          |          |          |           |          |               |
| RATIO CORRECT           | 190  | 0.3026   | 2.18593  | 1.14796  | 0.05415  | 0.15196   | 2.96968  | 0.57895       |

TODO : MEMORY USAGE

1. Sadia Afroz and Rachel Greenstadt. *PhishZoo: An Automated Web Phishing Detection Approach Based on Profiling and Fuzzy Matching*.

2. Valentino Aluigi. 2019. JavaScript implementation of the Average Hash using HTML5 Canvas.

3. R. Arandjelović and A. Zisserman. 2012. Three things everyone should know to improve object retrieval. In *2012 IEEE Conference on Computer Vision and Pattern Recognition*, 2911–2918. <https://doi.org/10.1109/CVPR.2012.6248018>

4. Omid Asudeh. A NEW REAL-TIME APPROACH FOR WEBSITE PHISHING DETECTION BASED ON VISUAL SIMILARITY. 53.

5. Herbert Bay, Tinne Tuytelaars, and Luc Van Gool. 2006. SURF: Speeded Up Robust Features. In *Computer Vision 2006*, Aleš Leonardis, Horst Bischof and Axel Pinz (eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 404–417. <https://doi.org/10.1007/11744023_32>

6. JiaWang Bian, Le Zhang, Yun Liu, Wen-Yan Lin, Ming-Ming Cheng, and Ian D. Reid. 2017. Image Matching: An Application-oriented Benchmark. *arXiv:1709.03917 \[cs\]*. Retrieved from <http://arxiv.org/abs/1709.03917>

7. Leonid Boytsov and Bilegsaikhan Naidan. 2013. Engineering Efficient and Effective Non-metric Space Library. In *Similarity Search and Applications*, David Hutchison, Takeo Kanade, Josef Kittler, Jon M. Kleinberg, Friedemann Mattern, John C. Mitchell, Moni Naor, Oscar Nierstrasz, C. Pandu Rangan, Bernhard Steffen, Madhu Sudan, Demetri Terzopoulos, Doug Tygar, Moshe Y. Vardi, Gerhard Weikum, Nieves Brisaboa, Oscar Pedreira and Pavel Zezula (eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 280–293. <https://doi.org/10.1007/978-3-642-41062-8_28>

8. Chomba Bupe. 2017. What algorithms can detect if two images/objects are similar or not? - Quora.

9. Hakan Cevikalp, Merve Elmas, and Savas Ozkan. 2018. Large-scale image retrieval using transductive support vector machines. *Computer Vision and Image Understanding* 173: 2–12. <https://doi.org/10.1016/j.cviu.2017.07.004>

10. K. Chen, J. Chen, C. Huang, and C. Chen. 2009. Fighting Phishing with Discriminative Keypoint Features. *IEEE Internet Computing* 13, 3: 56–63. <https://doi.org/10.1109/MIC.2009.59>

11. Qiang Chen, Zheng Song, Yang Hua, Zhongyang Huang, and Shuicheng Yan. 2012. Hierarchical matching with side information for image classification.

12. Matthijs Douze, Alexandre Sablayrolles, and Herve Jegou. 2018. Link and Code: Fast Indexing with Graphs and Compact Regression Codes. In *2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 3646–3654. <https://doi.org/10.1109/CVPR.2018.00384>

13. Yan Fang. 2012. Data Clustering and Graph-Based Image Matching Methods.

14. William T. Freeman, Antonio Torralba, Jenny Yuen, and Ce Liu. 2010. SIFT Flow: Dense Correspondence across Scenes and its Applications.

15. Aristides Gionis, Piotr Indyk, and Rajeev Motwani. Similarity Search in High Dimensions via Hashing. 12.

16. Nicolas Hahn. 2019. Differentiate images in python: Get a ratio or percentage difference, and generate a diff image - nicolashahn/diffimg.

17. C. Harris and M. Stephens. 1988. A Combined Corner and Edge Detector. In *Procedings of the Alvey Vision Conference 1988*, 23.1–23.6. <https://doi.org/10.5244/C.2.23>

18. Igor. 2011. Nuit Blanche: Are Perceptual Hashes an instance of Compressive Sensing ? *Nuit Blanche*.

19. Ahmet Iscen, Yannis Avrithis, Giorgos Tolias, Teddy Furon, and Ondrej Chum. 2018. Fast Spectral Ranking for Similarity Search. In *2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 7632–7641. <https://doi.org/10.1109/CVPR.2018.00796>

20. Jesse Kornblum. 2006. Identifying almost identical files using context triggered piecewise hashing. *Digital Investigation* 3: 91–97. <https://doi.org/10.1016/j.diin.2006.06.015>

21. Zhongyu Li, Xiaofan Zhang, Henning Müller, and Shaoting Zhang. 2018. Large-scale retrieval for medical image analytics: A comprehensive review. *Medical Image Analysis* 43: 66–84. <https://doi.org/10.1016/j.media.2017.09.007>

22. David G. Lowe. 2004. Distinctive Image Features from Scale-Invariant Keypoints. *International Journal of Computer Vision* 60, 2: 91–110. <https://doi.org/10.1023/B:VISI.0000029664.99615.94>

23. Gurmeet Singh Manku, Arvind Jain, and Anish Das Sarma. 2007. Detecting near-duplicates for web crawling. In *Proceedings of the 16th international conference on World Wide Web - WWW ’07*, 141. <https://doi.org/10.1145/1242572.1242592>

24. Andrey Nikishaev. 2018. Feature extraction and similar image search with OpenCV for newbies. *Medium*.

25. Ann Nurnajmin Qasrina, Dwi Pebrianti, Ibrahim Zuwairie, Bayuaji Luhur, and Mat Jusof Mohd Falfazli. 2018. Image Template Matching Based on Simulated Kalman Filter (SKF) Algorithm.

26. Aude Oliva and Antonio Torralba. Modeling the Shape of the Scene: A Holistic Representation of the Spatial Envelope. 31.

27. Jonathan Oliver, Chun Cheng, and Yanggui Chen. 2013. TLSH – A Locality Sensitive Hash. In *2013 Fourth Cybercrime and Trustworthy Computing Workshop*, 7–13. <https://doi.org/10.1109/CTC.2013.9>

28. Reshma Raj and Niya Joseph. 2016. Keypoint Extraction Using SURF Algorithm for CMFD.

29. Edward Rosten and Tom Drummond. 2006. Machine Learning for High-Speed Corner Detection. In *Computer Vision 2006*, Aleš Leonardis, Horst Bischof and Axel Pinz (eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 430–443. <https://doi.org/10.1007/11744023_34>

30. Ethan Rublee, Vincent Rabaud, Kurt Konolige, and Gary Bradski. 2011. ORB: An efficient alternative to SIFT or SURF. In *2011 International Conference on Computer Vision*, 2564–2571. <https://doi.org/10.1109/ICCV.2011.6126544>

31. Nikolaos Sarantinos, Chafika Benzaid, Omar Arabiat, and Ameer Al-Nemrat. 2016. Forensic Malware Analysis: The Value of Fuzzy Hashing Algorithms in Identifying Similarities. In *2016 IEEE Trustcom/BigDataSE/ISPA*, 1782–1787. <https://doi.org/10.1109/TrustCom.2016.0274>

32. Jingkuan Song, Lianli Gao, Li Liu, Xiaofeng Zhu, and Nicu Sebe. 2018. Quantization-based hashing: A general framework for scalable image and video retrieval. *Pattern Recognition* 75: 175–187. <https://doi.org/10.1016/j.patcog.2017.03.021>

33. Xudong Sun, Pengcheng Wu, and Steven C.H. Hoi. 2018. Face detection using deep learning: An improved faster RCNN approach. *Neurocomputing* 299: 42–50. <https://doi.org/10.1016/j.neucom.2018.03.030>

34. Sahil Suri, Peter Schwind, Johannes Uhl, and Peter Reinartz. 2010. Modifications in the SIFT operator for effective SAR image matching.

35. Shaharyar Ahmed Khan Tareen and Zahra Saleem. 2018. A comparative analysis of SIFT, SURF, KAZE, AKAZE, ORB, and BRISK. In *2018 International Conference on Computing, Mathematics and Engineering Technologies (iCoMET)*, 1–10. <https://doi.org/10.1109/ICOMET.2018.8346440>

36. Xuan Yang, Jihong Pei, and Jingli Shi. 2014. Inverse consistent non-rigid image registration based on robust point set matching.

37. Pengfei Yu. 2011. Image classification using latent spatial pyramid matching.

38. Wengang Zhou, Houqiang Li, Yijuan Lu, and Qi Tian. 2013. SIFT match verification by geometric coding for large-scale partial-duplicate web image search. *ACM Transactions on Multimedia Computing, Communications, and Applications* 9, 1: 1–18. <https://doi.org/10.1145/2422956.2422960>

39. Wengang Zhou, Yijuan Lu, Houqiang Li, Yibing Song, and Qi Tian. 2010. Spatial coding for large scale partial-duplicate web image search. In *Proceedings of the international conference on Multimedia - MM ’10*, 511. <https://doi.org/10.1145/1873951.1874019>

40. 2011. Looks Like It - The Hacker Factor Blog.

41. 2011. pHash-like image hash for java. *Pastebin.com*.

42. 2013. pHash.Org: Home of pHash, the open source perceptual hash library.

43. 2014. FAST Algorithm for Corner Detection 3.0.0-dev documentation.

44. 2014. Keypoints and Descriptors 1.

45. 2014. Introduction to SIFT (Scale-Invariant Feature Transform) 3.0.0-dev documentation.

46. 2014. ORB (Oriented FAST and Rotated BRIEF) 3.0.0-dev documentation.

47. 2015. Image Matching Using Generalized Scale-Space Interest Points.

48. 2015. BFMatcher raises error for Python interface when crossCheck option is enabled ⋅ Issue \#46 ⋅ MasteringOpenCV/code. *GitHub*.

49. 2016. Phishing Website Identification through Visual Clustering.

50. 2019. Fuzzy hashing API and fuzzy hashing tool. Contribute to ssdeep-project/ssdeep development by creating an account on GitHub.

51. 2019. Non-Metric Space Library (NMSLIB): An efficient similarity search library and a toolkit for evaluation of k-NN methods for generic non-metric spaces.: nmslib/nmslib.

52. 2019. A library for efficient similarity search and clustering of dense vectors.: facebookresearch/faiss.

53. Feature Matching + Homography to find Objects 3.0.0-dev documentation.

54. Spectralhashing.Pdf.

55. OpenCV: Feature Matching.

56. Testing different image hash functions.

57. Blockhash.

58. Toward a Phish Free World: A Cascaded Learning Framework for Phish Detection.

59. SIFT Flow: Dense Correspondence across Scenes and its Applications.

60. Java OpenCV - extracting good matches from knnMatch. *Stack Overflow*.

61. BRIEF (Binary Robust Independent Elementary Features) 3.0.0-dev documentation.
