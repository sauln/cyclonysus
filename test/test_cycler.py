import pytest
from collections import Counter

import numpy as np

from cyclenysus import Cycler

class TestCycler():
    def test_is_a_cycle(self):

        cycler = Cycler()
        data = np.random.random((100,3))

        cycler.fit(data)
        longest = cycler.longest_intervals(1)[0]
        cycle = cycler.get_cycle(longest)

        vertices = cycle.flatten()
        counts = Counter(vertices)
        
        return all([c == 2 for c in counts.values()])

    def test_longest_intervals(self):
        cycler = Cycler()
        data = np.random.random((100,3))

        cycler.fit(data)

        longest = cycler.longest_intervals(1)
        assert len(longest) == 1

        longest = cycler.longest_intervals(4)
        assert len(longest) == 4

