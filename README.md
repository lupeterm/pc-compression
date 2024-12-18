# pc-compression
Evaluation of point cloud geometry compression algorithms on sparse and non-uniform data.

## Rationale
In many real world robotics scenarios, point cloud geometries need to be exchanged between nodes in a system, e.g. the Robot Operating System (ROS). For instance, one of these nodes could be a Raspberry Pi that computes an unorganized point cloud (UPC) from a continuous stream of RGB-D data. Now, as this point cloud would be processed in in nodes further downstream inside the system, the entire UPC would have to be transmitted over a shared network between the nodes. 
Usually, the size of the point clouds grows quickly as the camera continues to perceive its surroundings. Furthermore, since bandwidth is often limited and expensive, geometric compression algorithms are necessary to ensure the application runs smoothly.

Compression of (point cloud) geometries has been extensively studied. A survey of relevant and recent literature concluded, that most publications evaluated their algorithms using very dense datasets in which the data points are uniformly placed, e.g. [8iVFB](http://plenodb.jpeg.org/pc/8ilabs). Conversely, a publication dedicated to the effective usage of compression algorithms on rather sparse and non-uniform geometries seems to be missing. 

As the raw amount of data in dense clouds is likely to be greater than its sparse counterpart, the analyses regarding processing time are naturally applicable. 
However, other factors may have been disregarded due to the focus on dense geometries. For instance, the amount of compression-induced information loss may play a different role when the data points are not spaced very close together. A lossy approach may even be favourable. Moreover, the underlying techniques predominantly used for dense geometries could show a different usefulness when applied to sparse ones.

The overarching idea of this project is to quantify the usage of geometric compression algorithms on sparse point clouds, thus evaluating
-  to which extent results of previous publications on dense data can generally be applied to sparse data,
- which (classes of) algorithms are most suitable,
- how useful *lossless* compression is in the context of sparse geometries, and
- if it is not sufficiently useful, at which point is it a valuable tradeoff?  

While outdoor or urban datasets are also valid, for the sake of setup simplicity, we will focus on indoor point clouds in this study. The next section presents a roadmap for the project including milestones and some additional technical information(datasets, algorithms, evaluation setup).


## Roadmap

1. Literature Review
   1. Algorithm qualifier
      1. Algorithm "Archetypes", e.g. 1D traversal, 2D mapping etc.
      2. amount of loss
      3. underlying technique
      4. type of input
      5. type of output
      6. (language/ needs (re-)implementation)
      7. Deterministic (?)
   2. Algorithms
      1.  Draco
      2.  pccomp
      3.  mpeg-pcc-tmc13 (?)
      4.  SarsePCGC (?)
      > Would like at least 4 algorithms
      > Likely have to implement my own (from a paper)
   3. Datasets
      1. Qualifiers
         1. Size
         2. Dynamic/Static
         3. Type of scenes
            1. Indoor/outdoor
            2. Synthetic / Realistic
         4. File format
      2. Datasets
         1. FIN Dataset
            > Record more scenes. Three were enough for the BA as a POC but here i cannot 2D-3D-S.
   4. Metrics
      1. bits per second (bps)
      2. peak signal to noise ration (PSNR)
      3. root mean square erro (RMSE)
      4. ?
2. Experimental Setup
   > probably Ros2 nodes
3. Evaluate
   > Gather all metrics and present them nicely using matplot or seaborn

## References
- [Google Draco](https://github.com/google/draco)
- [PCCOMP](https://github.com/szppaks/pccomp_oct)
- once i figure out how to use it, [mpeg-pcc-tmc13](https://github.com/MPEGGroup/mpeg-pcc-tmc13)
- [SparsePCGC](https://github.com/NJUVISION/SparsePCGC)
- [8iVFB](http://plenodb.jpeg.org/pc/8ilabs)