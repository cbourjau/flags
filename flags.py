"""
Treemap builder using pylab.

Uses algorithm straight from http://hcil.cs.umd.edu/trs/91-03/91-03.html

James Casbon 29/7/2006
"""

import pylab

import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data

im = plt.imread(get_sample_data('grace_hopper.jpg'))


class Treemap:
    def __init__(self, tree, iter_method, size_method, profile_pic):
        """create a tree map from tree, using itermethod(node) to walk tree,
        size_method(node) to get object size."""

        im = plt.imread(profile_pic)
        figsize = (10, 10)#(im.shape[0], im.shape[1])
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.imshow(im, zorder=0)
        self.ax.axis('off')
        pylab.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.size_method = size_method
        self.iter_method = iter_method
        self.addnode(tree)

    def addnode(self, node, lower=[0, 0], upper=[1, 1], axis=0):
        axis = axis % 2
        if isinstance(node, dict):
            self.draw_flag(lower, upper, node)
        width = upper[axis] - lower[axis]

        try:
            for child in self.iter_method(node):
                upper[axis] = lower[axis] + (width * float(size(child))) / size(node)
                self.addnode(child, list(lower), list(upper), axis + 1)
                lower[axis] = upper[axis]
        except TypeError:
            pass

    def draw_flag(self, lower, upper, node):
        newax = self.fig.add_axes([lower[0], lower[1], upper[0] - lower[0], upper[1] - lower[1]],
                                  anchor='NE', zorder=1)
        im = plt.imread(node['flag'])
        newax.imshow(im, aspect='auto', alpha=0.6)
        newax.axis('off')


def size(thing):
    if isinstance(thing, dict):
        return thing['cas']
    elif isinstance(thing, str):
        raise ValueError('dafuq')
    else:
        return reduce(int.__add__, [size(x) for x in thing])


def iter_method(thing):
    if isinstance(thing, dict):
        raise TypeError
    else:
        return iter(thing)


def make_tree(d):
    l = None
    for k, v in d.items():
        _ = list()
        _.insert(0, {'cas': v[0], 'flag': v[1]})
        if l:
            _.insert(1, tuple(l))
        l = tuple(_)
    return l

cas = {
    'afghanistan': [33165, 'images/Flag_of_Afghanistan.svg.png'],
    'iraq': [13509, 'images/Flag_of_Iraq.svg.png'],
    'nigeria': [10882 / 4, 'images/Flag_of_Nigeria.svg.png'],
    'cameroon': [10882 / 4, 'images/Flag_of_Cameroon.svg.png'],
    'niger': [10882 / 4, 'images/Flag_of_Niger.svg.png'],
    'chad': [10882 / 4, 'images/Flag_of_Chad.svg.png'],
    'syria': [46191, 'images/Flag_of_Syria.svg.png'],
    'somalia': [3724, 'images/Flag_of_Somalia.svg.png'],
    'sudan': [1139, 'images/Flag_of_Sudan.svg.png'],
    'pakistan': [3376, 'images/Flag_of_Pakistan.svg.png'],
    'mexico': [6028, 'images/Flag_of_Mexico.svg.png'],
    'libya': [2465, 'images/Flag_of_Libya.svg.png'],
    'yemen': [5720, 'images/Flag_of_Yemen.svg.png'],
    'france': [150, 'images/Flag_of_France.svg.png'],
    'ukraine': [3112, 'images/Flag_of_Ukraine.svg.png'],
}


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print "Usage: python flags.py profile_pic.jpg"
        quit()
    tree = make_tree(cas)
    Treemap(tree, iter_method, size, sys.argv[1])
    print "Total casualties in 2015: ", size(tree)
    plt.show()
