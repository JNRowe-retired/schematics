#!/usr/bin/env python


import copy
import unittest
import json

from expecter import expect

from schematics.models import (ModelOptions, _parse_options_config,
                               _gen_options, _extract_fields,
                               Model)
                               
from schematics.types.base import IntType


class TestOptions(unittest.TestCase):
    """This test collection covers the `ModelOptions` class and related
    functions.
    """
    def setUp(self):
        self._class = ModelOptions

    def tearDown(self):
        pass

    def test_good_options_args(self):
        args = {
            'klass': None,
            'db_namespace': None,
            'roles': None,
        }

        mo = self._class(**args)
        expect(mo) != None

        ### Test that a value for roles was generated
        expect(mo.roles) == {}
        expect(mo.roles) == {}

    def test_bad_options_args(self):
        args = {
            'klass': None,
            'db_namespace': None,
            'roles': None,
            'badkw': None,
        }
        with expect.raises(TypeError):
            self._class(**args)

    def test_no_options_args(self):
        args = {}
        mo = self._class(None, **args)
        expect(mo) != None

    def test_options_parsing(self):
        mo = ModelOptions(None)
        mo.db_namespace = 'foo'
        mo.roles = {}

        class Options:
            db_namespace = 'foo'
            roles = {}
            
        attrs = { 'Options': Options }
        oc = _parse_options_config(None, attrs, ModelOptions)

        expect(oc.__class__) == mo.__class__
        expect(oc.db_namespace) == mo.db_namespace
        expect(oc.roles) == mo.roles

    def test_options_parsing_from_model(self):
        class Foo(Model):
            class Options:
                db_namespace = 'foo'
                roles = {}
            
        class Options:
            db_namespace = 'foo'
            roles = {}
            
        attrs = { 'Options': Options }
        oc = _parse_options_config(Foo, attrs, ModelOptions)

        f = Foo()
        fo = f._options
        
        expect(oc.__class__) == fo.__class__
        expect(oc.db_namespace) == fo.db_namespace
        expect(oc.roles) == fo.roles


class TestMetaclass(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_extract_class_fields(self):
        bases = [Model]
        attrs = {'i': IntType()}
        
        fields = _extract_fields(bases, attrs)
        expect(attrs) == fields

    def test_bad_extract_class_fields(self):
        bases = []
        attrs = {'i': 5}
        expected = {'i': IntType()}
        
        fields = _extract_fields(bases, attrs)
        expect(expected) != fields

    def test_extract_subclass_fields(self):
        class Foo(Model):
            x = IntType()
            y = IntType()
            z = 5  # should be ignored

        bases = [Foo]
        attrs = {'i': IntType()}

        fields = _extract_fields(bases, attrs)
        expected = {
            'i': attrs['i'],
            'x': Foo.x,
            'y': Foo.y,
        }
        expect(fields) == expected


class TestModels(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_equality(self):
        class TestModel(Model):
            some_int = IntType()

        tm1 = TestModel()
        tm1.some_int = 4
        expect(tm1) == copy.copy(tm1)

        tm2 = TestModel()
        tm2.some_int = 4
        expect(tm1) == tm2

    def test_model_field_list(self):
        it = IntType()
        class TestModel(Model):
            some_int = it
        
        expect({'some_int': it}) == TestModel._fields

    def test_model_data(self):
        class TestModel(Model):
            some_int = IntType()

        with expect.raises(AttributeError):
            TestModel._data()
        
    def test_instance_data(self):
        class TestModel(Model):
            some_int = IntType()

        tm = TestModel()
        tm.some_int = 5
        
        expect({'some_int': 5}) == tm._data

    def test_dict_interface(self):
        class TestModel(Model):
            some_int = IntType()

        tm = TestModel()
        tm.some_int = 5
        
        expect(tm).contains('some_int')
        expect(tm['some_int']) == 5
        expect(tm).does_not_contain('fake_key')
        
        
