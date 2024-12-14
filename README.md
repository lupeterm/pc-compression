# pc-compression
Evaluation of point cloud geometry compression algorithms on sparse and non-uniform data.

## Rationale
A survey of recent and relevant literature concluded that most algorithms are tested on very dense geometries.
While this may give an accurate description of an algorithm's efficiency, real-world data may oftentimes not be as dense and uniformly spaced.
Therefore, it is useful to investigate an array of things:
- which algorithms are even useful on sparse data?
- is lossless compression of realistic clouds necessary?
- if not, is there an optimal value of loss considering computation effort and output error?
- ...

## Roadmap

1. TODO Algorithm Survey
    > Draco, pccomp
    > Would like at least 4 algorithms
    > Likely have to implement my own (from a paper)
2. Experimental Setup
   1.  Which Datasets? 
   > Probably my own
   2.  TODO Which metrics?
   3.  General Experiment Design
   > Probably going to write ROS II nodes 
3. Evaluate
   > Gather all metrics and present them nicely using matplot or seaborn

## References
Google Draco: https://github.com/google/draco\
PCCOMP: https://github.com/szppaks/pccomp_oct\
once i figure out how to use it, mpeg-pcc-tmc13 : https://github.com/MPEGGroup/mpeg-pcc-tmc13