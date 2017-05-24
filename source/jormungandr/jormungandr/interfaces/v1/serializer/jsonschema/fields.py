# coding=utf-8

# Copyright (c) 2001-2014, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

import serpy


def _init(self, parent_class, schema_type=None, schema_metadata={}, **kwargs):
    """
    Call the parent constructor with the needed kwargs and 
    add the remaining kwargs to the schema metadata
    """
    if 'display_none' not in kwargs:
        kwargs['display_none'] = False
    parent_vars = set(parent_class.__init__.func_code.co_names)
    parent_kwargs = {k: v for k, v in kwargs.items() if k in parent_vars}
    remaining_kwargs = {k: v for k, v in kwargs.items() if k not in parent_vars}
    parent_class.__init__(self, **parent_kwargs)
    self.schema_type = schema_type
    self.schema_metadata = schema_metadata or {}
    # the remaining kwargs are added in the schema metadata to add a bit of syntaxic sugar
    self.schema_metadata.update(**remaining_kwargs)


class Field(serpy.Field):
    """
    A :class:`Field` that hold metadata for schema.
    """
    def __init__(self, schema_type=None, schema_metadata=None, **kwargs):
        _init(self, serpy.Field, schema_type=schema_type or str, schema_metadata=schema_metadata, **kwargs)


class StrField(serpy.StrField):
    """
    A :class:`StrField` that hold metadata for schema.
    """

    def __init__(self, schema_metadata=None, **kwargs):
        _init(self, serpy.StrField, schema_type=str, schema_metadata=schema_metadata, **kwargs)


class BoolField(serpy.BoolField):
    """
    A :class:`BoolField` that hold metadata for schema.
    """

    def __init__(self, schema_metadata=None, **kwargs):
        _init(self, serpy.BoolField, schema_type=bool, schema_metadata=schema_metadata, **kwargs)


class FloatField(serpy.FloatField):
    """
    A :class:`FloatField` that hold metadata for schema.
    """

    def __init__(self, schema_metadata=None, **kwargs):
        _init(self, serpy.FloatField, schema_type=float, schema_metadata=schema_metadata, **kwargs)


class IntField(serpy.IntField):
    """
    A :class:`IntField` that hold metadata for schema.
    """

    def __init__(self, schema_metadata=None, **kwargs):
        _init(self, serpy.IntField, schema_type=int, schema_metadata=schema_metadata, **kwargs)


class MethodField(serpy.MethodField):
    """
    A :class:`MethodField` that hold metadata for schema.
    """

    def __init__(self, method=None, schema_type=None, schema_metadata=None, **kwargs):
        kwargs['method'] = method
        _init(self, serpy.MethodField, schema_type=schema_type, schema_metadata=schema_metadata, **kwargs)
