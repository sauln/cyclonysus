# Cyclenysus

This is a very lightweight wrapper that hides all the headaches of extracting representative cycles from persistence diagrams.

There are no guarantees that this library is fast, well written, or correct. If you find issues, please create a github issue or pull request.

# Setup

This library is a wrapper around Dionysus and Dionysus requires Boost to work properly. If you have Boost, then you can install easily.

```
git clone https://github.com/sauln/cyclenysus
pip install -e .
```


# Usage

First, construct a diagram. In this example, we will use [Ripser](https://github.com/sauln/ripser).

First generate some data, one big circle and some noise stuff a ways away.

``` Python
import numpy as np
from sklearn import datasets

data, _ = datasets.make_circles(40)
data = np.concatenate([data,np.random.random((30,2))+3])
```

Then generate the persistence diagrams, longest 3 cycles, and vertex sets.

``` Python
from cyclenysus import Cycler

cycler = Cycler()
cycler.fit(data)

top_intervals = cycler.longest_intervals(3)
cycles = [cycler.get_cycle(interval) for interval in top_intervals]

vertex_sets = [cycler.order_vertices(cycle) for cycle in cycles]
```

Then we can visualize our cycles.

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
