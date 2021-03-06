## Requirements

In any case:

- Docker. You may get it [here](https://docs.docker.com/install/)
- Update docker memory limit if necessary
- Git
- Clone the repo `git clone git@github.com:ikhlestov/deployml.git`

For local setup you will also need:

- Python >= 3.5
- Bazel ([installation manual](https://docs.bazel.build/versions/master/install.html))
- Tensorflow source code `git clone https://github.com/tensorflow/tensorflow.git`

## Local SetUp

1. Create virtual env
    - `python3.6 -m venv .venv && source .venv/bin/activate`
    - or `python3 -m venv .venv --without-pip && source .venv/bin/activate && wget https://bootstrap.pypa.io/get-pip.py -P /tmp/ && python /tmp/get-pip.py`
2. Install required packages according to your OS:

    - Ubuntu - `pip install -r requirements/local_ubuntu.txt`
    - Mac - `pip install -r requirements/local_mac.txt`

## Docker SetUp

### Pull containers

`docker pull ikhlestov/deployml_dev`

### Build containers

*You don't need first step if you've pulled container successfully*

- Dev container `docker build -f dockers/Dev . -t ikhlestov/deployml_dev`
- Dev container `docker build -f dockers/ProdLarge . -t deployml_prod_large`
- Dev container `docker build -f dockers/ProdSmall . -t deployml_prod_small`
- Compare their sizes `docker images | grep "deployml_dev\|deployml_prod_large\|deployml_prod_small"`

<!---
Don't forget about `.dockerignore` file.
Try to organize your docker file to use cache as much as possible.
Develop with ubuntu, release with some smaller distros.
-->

## Start with various frameworks

- Check defined models in the `models` folder
- Run docker container with mounted directory `docker run -v $(pwd):/deployml -it ikhlestov/deployml_dev /bin/bash`
- Run time measurements inside docker `cd /deployml && python3.6 benchmarks/compare_frameworks.py`
- Run time measurements for every model locally `python3.6 benchmarks/compare_frameworks.py`(if you've passed local setup)

## Optimize tensorflow

- Build frozen graph with `python3.6 optimizers/get_frozen_graph.py`. More about it you may read [here](https://blog.metaflow.fr/tensorflow-how-to-freeze-a-model-and-serve-it-with-a-python-api-d4f3596b3adc)
- Compare frozen graph with usual one `python3.6 benchmarks/compare_frozen_graph.py`
- Build optimized frozen graph `python3.6 optimizers/get_optimized_frozen_graph.py`
- Check what speedup we've got `python3.6 benchmarks/compare_optimized_graph.py`
- Get quantized graph `chmod +x optimizers/quantize_model.sh && ./optimizers/quantize_model.sh`
- Is it faster? `python3.6 benchmarks/compare_quantized_graph.py`

For model quantization you need compiled tensorflow methods. They are already exist in docker, but in case you want to do it manually:

- install bazel ([manual](https://docs.bazel.build/versions/master/install.html))
- clone tensorflow repo `git clone https://github.com/tensorflow/tensorflow.git && cd tensorflow`
- build required script `bazel build tensorflow/tools/graph_transforms:transform_graph`

<!---
The main usability that you may ship your model as one binary file.
You should freeze/optimize/serve model with the same tensorflow version.
Quantization may reduce model size, but also decrease model speed.
-->

You may also take a look at other methods ([list of resources](resources.md)) like:

- More about pruning
- Quantization
- XNOR nets
- Knowledge distillation

## Try various restrictions

- CPU restriction `docker run -v $(pwd):/deployml -it --cpus="1.0" ikhlestov/deployml_dev /bin/bash`
- Memory restriction `docker run -v $(pwd):/deployml -it --memory=1g ikhlestov/deployml_dev /bin/bash`
- Try to run two models on two different CPUs
- Try to run two models on two CPU simultaneously

<!---
Where data preprocessing should be done? CPU or GPU or even another host?
-->


## Preprocessing and testing

Q: Where is preprocessing should be done - on CPU or GPU?

- enter to the preprocessing directory `cd preprocessing`
- run various resizers benchmarks `python3.6 benchmark.py`
    
    - Note: opencv may be installed from PyPi for python3

- check unified resizer at the `image_preproc.py`
- try to run tests for it `pytest test_preproc.py`(and they will fail)
- fix resizer
- run tests again `pytest test_preproc.py`

What else should be tested(really - as much as possible):

- General network inference
- Model loading/saving
- New models deploy
- Any preprocessing
- Corrupted inputs - Nan, Inf, zeros
- Determinism
- Input ranges/distributions
- Output ranges/distributions
- Test that model will fail in known cases
- ...
- Just check [this video](https://youtu.be/T_YWBGApUgs?t=5h59m40s) :)

You my run tests:

- At the various docker containers
- Under the [tox](https://tox.readthedocs.io/en/latest/)

## Converting to the tensorflow

- Converting from keras to tensorflow:

    - Get keras saved model `python3.6 converters/save_keras_model.py`
    - Convert keras model to the tensorflow save format `python3.6 converters/convert_keras_to_tf.py`

- Converting from PyTorch to tensorflow:

    - Trough keras - [converter](https://github.com/nerox8664/pytorch2keras)
    - Manually

In any case you should know about:

- [Open Neural Network Exchange](https://github.com/onnx/onnx)
- [Deep Learning Model Convertors](https://github.com/ysh329/deep-learning-model-convertor)

## Build back-end server

- One-to-one server
- Scaling with multiprocessing
- Queues based(Kafka, RabbitMQ, etc)
- Serving with [tf-serving](https://www.tensorflow.org/serving/)

## Profiling

- Code:
    
    - [Line profiler](https://github.com/rkern/line_profiler)
    - [CProfile](https://docs.python.org/3.6/library/profile.html)
    - [PyCharm Profiler](https://www.jetbrains.com/help/pycharm/optimizing-your-code-using-profilers.html)

- Tensorflow:

    - [Chrome trace format based](https://towardsdatascience.com/howto-profile-tensorflow-1a49fb18073d)
    - [Tf benchmark tool](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/benchmark)
    - [Tf benchmark class](https://www.tensorflow.org/api_docs/python/tf/test/Benchmark)

- CPU/GPU:

    - nvidia-smi
    - [gpustat](https://github.com/wookayin/gpustat)
    - [psutil](https://pypi.python.org/pypi/psutil)
    - [nvidia profiler](https://developer.nvidia.com/nvidia-visual-profiler)

- Lifetime benchmark - [airspeed velocity](https://github.com/airspeed-velocity/asv)

## Automation

- Continuous integration:

    - Jenkins
    - Travis
    - TeamCity
    - CircleCI

- Clusters:

    - Kubernetes
    - Mesos
    - Docker swarm

- Configuration management:

    - Terraform
    - Ansible
    - Chef
    - Puppet
    - SaltStack

## Conclusion

I'm grateful for cool ideas to Alexandr Onbysh, Aleksandr Obednikov and Kyryl Truskovskyi.

Take a look at the [checklist](checklist.md).

Thank you for reading!
