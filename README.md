[![Build Status](https://travis-ci.org/sauln/cyclenysus.svg?branch=master)](https://travis-ci.org/sauln/cyclenysus)
[![codecov](https://codecov.io/gh/sauln/cyclenysus/branch/master/graph/badge.svg)](https://codecov.io/gh/sauln/cyclenysus)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Cyclenysus

This is a very lightweight library that hides all the headaches of extracting representative cycles from persistence diagrams. 

Cyclenysus currently sits on top of Dionysus, but hides almost everything from you. All you have to worry about is your numpy arrays.

There are no guarantees that this library is fast, well written, or correct. If you find issues, please create a github issue or pull request. It is currently only tested for 1-cycles.

## Setup

This library is a wrapper around Dionysus and Dionysus requires Boost to work properly. If you have Boost, then you can install Cyclenysus easily.

```
git clone https://github.com/sauln/cyclenysus
pip install -e .
```

## Usage

First, construct a diagram. In this example, we will use [Ripser](https://github.com/sauln/ripser).

### First generate some data. 

Create one big noise circle and a noisy blob nearby.

``` Python
import numpy as np
from sklearn import datasets

data, _ = datasets.make_circles(40)
data = np.concatenate([data,np.random.random((30,2))+3])
```

![raw data, one noise circle with another blob nearby][dataset]

Then, we'll generate the persistence diagram for $H_1$ for this data.  Using persistence diagram, we can extract the longest 3 cycles and vertex sets of each cycle.

``` Python
from cyclenysus import Cycler

cycler = Cycler()
cycler.fit(data)

top_intervals = cycler.longest_intervals(3)
cycles = [cycler.get_cycle(interval) for interval in top_intervals]

vertex_sets = [cycler.order_vertices(cycle) for cycle in cycles]
```

Using `ripser`, the generated persistence diagram looks like

![persistence diagram for H1. One point far from the diagonal][persistence-diagram]

Let's take a look at the cycles we generated overlaid on the original data. In the image below, the longest interval corresponds to the cycle around the main circle, just as we would expect.

``` Python
# Plot cycle
for vertices in vertex_sets:
    xs_v, ys_v = data[vertices][:,0], data[vertices][:,1]
    plt.plot(xs_v, ys_v)

# Plot data
xs, ys = data[:,0], data[:,1]
plt.scatter(xs, ys)
plt.show()
```

![multiple cycles on dataset][multiple-cycles]

Checkout the notebook [Computing Cycles.ipynb](notebooks/Compute Cycles.ipynb) for an executable example.


<!-- Images -->
[persistence-diagram]: docs/images/persistence_diagram.png
[dataset]: docs/images/data_with_noisy_circle.png
[multiple-cycles]: docs/images/multiple-cycles.png "Multiple cycles on dataset"

