#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import config as c

sns.set_style('darkgrid')

def check_pattern(entries):
    """Find the pattern of the given data

    Examples:
        check_pattern(['0', '1', '2', '0', '1', '2'])
        >>> 2
        check_pattern(['0', '1', '2', '0', '1'])
        >>> 1
        check_pattern(['0', '1', '2', '1', '2', '2'])
        >>> 1

    Args:
        entries: a list of entries

    Returns:
        how many piece(s) the data should be splitted into, int.
    """
    d = {}
    for n in entries:
        if n in d:
            d[n] += 1
        else:
            d[n] = 1

    if all(value == d[entries[0]] and value > 1 for value in d.values()):
        return d[entries[0]]
    else:
        return 1


def read_input(path):
    """Read input from a given file and repack it to return as generator of list.

    Args:
        path: string, relative or complete path of the input file.

    Returns:
        generator of list, containing all values of each entry that need to be plotted in inner lists.

    """
    entries = []
    values = []
    with open(path, 'r') as file:
        for line in file:
            unpacked = line.split()
            entries.append(unpacked[0])
            values.append(unpacked[1:])

    num_slices = check_pattern(entries)
    step = len(entries) // num_slices
    for i in range(num_slices):
        yield [[float(v) for v in one_list] for one_list in values[step * i:step * (i + 1)]]


def draw_plot(data, labels, titles, interval_x, interval_y=None, xy_labels=None, orientation='h', one_plot=True, save_path=None):
    """Customized function for drawing plots from the given data.

    Args:
        data       : list of list, containing the major values that are going to be plotted;
        labels     : list of string, containing the labels along to all lines in plot;
        titles     : list of string, containing the titles for each subplot;
        interval_x : list of 2 float, the first is the start while the second is the end of x;
        interval_y : list of 2 float, the first is the start while the second is the end of y;
        xy_labels  : list of 2 string, the first is the name for x axis while the second is the name for y axis;
        orientation: string, either 'h' or 'v', plot in `horizontal` or `vertical` respectively;
        one_plot   : boolean, if True plot in one whole figure; otherwise plot in a couple of subplot; 
        save_path  : string, if None just show plot at the end; otherwise save plot in the given path.

    Returns:
        None
    """
    import numpy as np

    xy_labels = ['', ''] if xy_labels == None else xy_labels

    def plot_in_one():
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title(titles[0])

        try:
            for l, value in enumerate(next(data)):
                x = np.linspace(interval_x[0], interval_x[1], num=len(value))
                ax.plot(x, value, label=labels[l])
                ax.set_xlabel(xy_labels[0])
                ax.set_ylabel(xy_labels[1])
                ax.set_xlim(interval_x[0], interval_x[1])
                if interval_y != None:
                    ax.set_ylim(interval_y[0], interval_y[1])
                ax.legend()
        except StopIteration:
            print("Gone through all data.")
        finally:
            fig.tight_layout()
            
            if not save_path:
                plt.show()
            else:
                fig.savefig(save_path)

    def plot_in_more(num_subplot):
        if orientation == 'h':
            fig = plt.figure(figsize=(num_subplot * 6, 5))
        elif orientation == 'v':
            fig = plt.figure(figsize=(6, num_subplot * 3))

        for i in range(len(titles)):

            if orientation == 'h':
                ax = fig.add_subplot(1, num_subplot, i + 1)
            elif orientation == 'v':
                ax = fig.add_subplot(num_subplot, 1, i + 1)

            ax.set_title(titles[i])
            try:
                for l, value in enumerate(next(data)):
                    x = np.linspace(
                        interval_x[0], interval_x[1], num=len(value))
                    ax.plot(x, value, label=labels[l])
                    ax.set_xlabel(xy_labels[0])
                    ax.set_ylabel(xy_labels[1])
                    ax.set_xlim(interval_x[0], interval_x[1])
                    if interval_y != None:
                        ax.set_ylim(interval_y[0], interval_y[1])
                    ax.legend()
            except StopIteration:
                print("Gone through all data")
        fig.tight_layout()

        if not save_path:
            plt.show()
        else:
            fig.savefig(save_path)

    if not one_plot:
        plot_in_more(len(titles))
    else:
        plot_in_one()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        assert os.path.isfile(
            input_file), "The file you provide doesn't exist. Please check it again."
        values = read_input(input_file)

    elif len(sys.argv) == 1:
        values = read_input(c.input_file)

    if c.save_path:
        assert (".png" == c.save_path[-4:]) or (".pdf" == c.save_path[-4:]), \
            "The file extension you provide is not valid. Just accept \'.png\' and \'.pdf\'"

    draw_plot(values, c.labels, c.titles, c.interval_x, 
              interval_y=c.interval_y, xy_labels=c.xy_labels,
              orientation=c.orientation, one_plot=c.one_plot, save_path=c.save_path)
