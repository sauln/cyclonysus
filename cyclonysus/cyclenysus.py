import numpy as np
import dionysus

class Cycler:
    """ Build a rips diagram of the data and and provide access to cycles.

        This class wraps much of the functionality in Dionysus, giving it a clean interface and providing a way to access cycles.

        Warning: This has only been tested to work for 1-cycles. 
    """
    
    def __init__(self, order=1):
        self.order = order
        self.barcode = None
        self.cycles = None
        
        self._diagram = None
        self._filtration = None
        
    def fit(self, data):
        """ Generate Rips filtration and cycles for data.
        """

        # Generate rips filtration 
        maxeps = np.max(data.std(axis=0)) # TODO: is this the best choice?
        cpx = dionysus.fill_rips(data, self.order+1, maxeps)

        # Add cone point to force homology to finite length; Dionysus only gives out cycles of finite intervals
        spxs = [dionysus.Simplex([-1])] + [c.join(-1) for c in cpx]
        for spx in spxs:
            spx.data = 1
            cpx.append(spx)

        # Compute persistence diagram
        persistence = dionysus.homology_persistence(cpx)
        diagrams = dionysus.init_diagrams(persistence, cpx)

        # Set all the results
        self._filtration = cpx
        self._diagram = diagrams[self.order]
        self._persistence = persistence
        self.barcode = np.array([(d.birth, d.death) for d in self._diagram])

        self._build_cycles()

    def _build_cycles(self):
        """Create cycles from the diagram of order=self.order
        """
        cycles = {}
        
        intervals = sorted(self._diagram, key=lambda d: d.death-d.birth, reverse=True)

        for interval in self._diagram:
            if self._persistence.pair(interval.data) != self._persistence.unpaired:
                cycle_raw = self._persistence[self._persistence.pair(interval.data)]
                
                # Break dionysus iterator representation so it becomes a list
                cycle = [s for s in cycle_raw]
                cycle = self._data_representation_of_cycle(cycle)
                cycles[interval.data] = cycle
        
        self.cycles = cycles

    def _data_representation_of_cycle(self, cycle_raw):
        cycle = np.array([list(self._filtration[s.index]) for s in cycle_raw])    
        return cycle

    def get_cycle(self, interval):
        """Get a cycle for a particular interval. Must be same type returned from `longest_intervals` or entry in `_diagram`.
        """

        return self.cycles[interval.data]
    
    def get_all_cycles(self):
        return list(self.cycles.values())
    
    def longest_intervals(self, n):
        """Return the longest n intervals. For all intervals, just access diagram directly from _diagram.
        """

        intervals = sorted(self._diagram, key=lambda d: d.death-d.birth, reverse=True)
        return intervals[:n]
    
    def order_vertices(self, cycle):
        """ Take a cycle and generate an ordered list of vertices.

            This representation is much more useful for analysis.
        """
        ordered_vertices = [cycle[0][0], cycle[0][1]]
        next_row = 0

        # TODO: how do I make this better? It seems so hacky
        for _ in cycle[1:]:
            next_vertex = ordered_vertices[-1]
            rows, cols = np.where(cycle == next_vertex)
            which = np.where(rows != next_row)
            next_row, next_col = rows[which], (cols[which] + 1) % 2

            ordered_vertices.append(cycle[next_row,next_col][0])
        
        return ordered_vertices

