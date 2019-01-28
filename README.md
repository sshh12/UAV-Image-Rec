# target-finder-model

> Contains files needed to create the model for
> [target-finder](https://github.com/uavaustin/target-finder)

[![CircleCI](https://circleci.com/gh/uavaustin/target-finder-model/tree/master.svg?style=svg)](https://circleci.com/gh/uavaustin/target-finder-model/tree/master)


## Developer Instructions

### Install
1. Download `git clone https://github.com/uavaustin/target-finder-model`
2. Get Darknet (requires Linux or [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10))
    * `cd target-finder-model && git clone https://github.com/AlexeyAB/darknet.git`
    * `cd darknet` and edit `MakeFile`
        * If CPU `AVX=1` `OPENMP=1` `LIBSO=1`
        * If GPU `GPU=1` `CUDNN=1` `LIBSO=1`
        * `make`
    * Download this [darknet53.conv.74](https://pjreddie.com/media/files/darknet53.conv.74)

### Generate
* `python generate/pull_assets.py` Download base shapes and background images
* `python generate/create_full_images.py` Create full-sized artificial images
* `python generate/create_clf_data.py` Convert full-sized images to training data for classifier
* `python generate/create_detection_data.py` Convert full-sized images to training data for detection model

### Training
* `source scripts/train-detector.sh` Train detection model
* `source scripts/train-preclf.sh` Train classifier model

## Testing

To run the tests, first install `tox`.

```sh
$ pip3 install tox
```

Now the tests can be run by simply calling:

```sh
$ tox
```

This takes care of installing the development dependencies in a Python virtual
environment. After, it runs quick unit tests to ensure the model
file is loading as expected.

To only build the shapes and run the training step, or run the unit tests, you
can run `tox -e model` and `tox -e unit`, respectively.

These tests are automatically run on CircleCI on each commit.

## Releases

Building the full model is managed with CircleCI (along with the testing
above).

Full builds are run on tags and the model is uploaded as a build artifact at
the end and pushed to GitHub Releases.
