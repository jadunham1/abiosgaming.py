"""Useful utilities"""
import collections


def named_tuple(mapping):
    """
    Function to turn a collections.Mapping into a namedtuple of namedtuples

    Takes dict, collections.defaultdict,
    collections.OrderedDict, or collections.Counter
    recursively turn it into a named_tuple

    :param mapping: object to be converted to namedtuple
    :rtype: collections.namedtuple of collections.namedtuple
    """
    if (isinstance(mapping, collections.Mapping)):
        for key, value in mapping.items():
            mapping[key] = named_tuple(value)
        return namedtuple_from_mapping(mapping)
    return mapping


def namedtuple_from_mapping(mapping, name="NamedTuple"):
    """
    Function to take a mpping and created a namedtuple

    :param mapping: mapping to be converted to namedtuple
    :rtype: namedtuple
    """
    this_namedtuple_maker = collections.namedtuple(name, mapping.keys())
    return this_namedtuple_maker(**mapping)
