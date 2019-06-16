# UAV Image Recognition

> A snapshot of the code used by the [Unmanned Aerial Vehicle Team at Austin (UAVA)](https://uavaustin.org) for image recognition tasks.

![banner](https://user-images.githubusercontent.com/6625384/58374531-6fdf9b00-7f05-11e9-9d2c-e51c024209d5.jpg)

## Tech

#### target-finder-model

`target-finder-model` contains:
* Scripts to generate fake test imagery with labels for training
* A [CNN](https://en.wikipedia.org/wiki/Convolutional_neural_network) model for filtering imagery that either may contain or does not contain a target
* A [darknet](https://github.com/AlexeyAB/darknet) implementation of [YOLOv3](https://pjreddie.com/darknet/yolo/) for detecting the location of targets as well as their characteristics (writing, shape, etc)
* Hyperparams, configs, training scripts for both models

#### target-finder

`target-finder` contains:
* Scripts which preprocess raw imagery for the models
* The inference code for detection and interpretation of the models output in an actionable format
* An easy to use `find_targets(image)` API

## Originial Repos

* [uavaustin/target-finder](https://github.com/uavaustin/target-finder)
* [uavaustin/target-finder-model](https://github.com/uavaustin/target-finder-model)

##### Primary Contributors 

* [@bbridges](https://github.com/bbridges)
* [@sshh12](https://github.com/sshh12)
* [@alexwitt2399](https://github.com/alexwitt2399)
* [@yhylord](https://github.com/yhylord)
* [@kadhirumasankar](https://github.com/kadhirumasankar)
