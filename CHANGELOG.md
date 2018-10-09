# Changelog

## v0.2.0 (in development)

### Features

- Model built with new shape generation system.
- Shape generation is deterministic.

### Breaking Changes

- This model is _*not*_ compatible with `v0.1.0` since this model was built
  with a newer version of the `retrain.py` script for the Inception V3 model.

### Chores

- Fetch assets hosted on Bintray.
- Parallelize the shape generation in threads.
- Build on the model on CircleCI to speed up build times.

## v0.1.0 (2018-08-02)

Initial release.
