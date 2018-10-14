# target-finder-model

> Contains files needed to create the model for
> [target-finder](https://github.com/uavaustin/target-finder)

[![CircleCI](https://circleci.com/gh/uavaustin/target-finder-model/tree/master.svg?style=svg)](https://circleci.com/gh/uavaustin/target-finder-model/tree/master)

*Models are released in tar archives with Github Releases. Model versions do
not necessarily correspond to a target-finder version.*

## Building the Model

The build process for the model is broken up into 4 steps:

- Pulling assets needing for NAS and shape generation
- Creating NAS (Not-A-Shape) images
- Creating shape images
- Retraining the Inception V3 Model with the images above

To build, first you'll need to install the development dependencies.

```sh
$ pip3 install -r requirements-dev.txt
```

The entire build process can be done by running `build.py`:

```sh
$ ./build.py
```

Configuration settings for how the model can be built are in
`generate/config.py`. Some of these can be adjusted on the command-line with
environment variables.

For example, to build 1000 shapes (instead of the default 5000), you can set
the `NUM_SHAPES` environment variable. This will produce 1000 NAS images as
well.

```sh
$ NUM_SHAPES=1000 ./build.py
```

By default, shape generation will run in twice as many threads as CPUs. This
allows for much faster shape generation at the expensive of very high CPU
usage. You can run the shape generation in one thread as well:

```sh
$ NUM_THREADS=1 ./build.py
```

Shape output will be in `generate/shapes` and is separated by shape type. The
final result of training is put into the `target_finder_model/data` folder. You
can run `pip3 install -e .` to install this as a development library and use
the `target-finder` library to check model accuracy.

See `generate/config.py` for more configuration options.

The individual processes can be run separately by running the following files:

- `generate/pull_assets.py`
- `generate/nas_gen.py`
- `generate/shape_gen.py`
- `generate/train.py`

Note that NAS and Shape generation is deterministic. Deleting the output and
running the generation again will produce the exact same images.

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
environment, and then runs the build process but with only 100 of each shape
instead of the full batch. After, it runs quick unit tests to ensure the model
file is loading as expected.

To only build the shapes and run the training step, or run the unit tests, you
can run `tox -e model` and `tox -e unit`, respectively.

These tests are automatically run on CircleCI on each commit, and will attach
the shapes as a build artifact.

## Releases

Building the full model is managed with CircleCI (along with the testing
above). Note that the full-sized shape generation might take around 2 or more
hours, assuming a 4-core machine, and using 8 threads. This is parallelized in
the CI environment, giving faster builds.

Full builds are run on tags and the model is uploaded as a build artifact at
the end and pushed to GitHub Releases.
