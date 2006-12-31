import unittest
import nose
import nose.case
from nose.util import absfile

class TestUtils(unittest.TestCase):
    
    def test_file_like(self):
        assert nose.file_like('a/file')
        assert nose.file_like('file.py')
        assert nose.file_like('/some/file.py')
        assert not nose.file_like('a.file')
        assert not nose.file_like('some.package')
        
    def test_split_test_name(self):
        assert nose.split_test_name('a.package:Some.method') == \
            (None, 'a.package', 'Some.method')
        assert nose.split_test_name('some.module') == \
            (None, 'some.module', None)
        assert nose.split_test_name('this/file.py:func') == \
            ('this/file.py', None, 'func')
        assert nose.split_test_name('some/file.py') == \
            ('some/file.py', None, None)
        assert nose.split_test_name(':Baz') == \
            (None, None, 'Baz')

    def test_split_test_name_windows(self):
        # convenience
        stn = nose.split_test_name
        self.assertEqual(stn(r'c:\some\path.py:a_test'),
                         (r'c:\some\path.py', None, 'a_test'))
        self.assertEqual(stn(r'c:\some\path.py'),
                         (r'c:\some\path.py', None, None))
        self.assertEqual(stn(r'c:/some/other/path.py'),
                         (r'c:/some/other/path.py', None, None))
        self.assertEqual(stn(r'c:/some/other/path.py:Class.test'),
                         (r'c:/some/other/path.py', None, 'Class.test'))
        try:
            stn('c:something')
        except ValueError:
            pass
        else:
            self.fail("Ambiguous test name should throw ValueError")
        
    def test_test_address(self):
        # test addresses are specified as
        #     package.module:class.method
        #     /path/to/file.py:class.method
        # converted into 3-tuples (file, module, callable)
        # all terms optional
        class Foo:
            def bar(self):
                pass
        def baz():
            pass

        f = Foo()

        class FooTC(unittest.TestCase):
            def test_one(self):
                pass
            def test_two(self):
                pass
        
        foo_funct = nose.case.FunctionTestCase(baz)
        foo_functu = unittest.FunctionTestCase(baz)

        foo_mtc = nose.case.MethodTestCase(Foo, 'bar')

        me = absfile(__file__)
        self.assertEqual(nose.test_address(baz),
                         (me, __name__, 'baz'))
        assert nose.test_address(Foo) == (me, __name__, 'Foo')
        assert nose.test_address(Foo.bar) == (me, __name__,
                                              'Foo.bar')
        assert nose.test_address(f) == (me, __name__, 'Foo')
        assert nose.test_address(f.bar) == (me, __name__, 'Foo.bar')
        assert nose.test_address(nose) == (absfile(nose.__file__), 'nose')

        # test passing the actual test callable, as the
        # missed test plugin must do
        self.assertEqual(nose.test_address(FooTC('test_one')),
                         (me, __name__, 'FooTC.test_one'))
        self.assertEqual(nose.test_address(foo_funct),
                         (me, __name__, 'baz'))
        self.assertEqual(nose.test_address(foo_functu),
                         (me, __name__, 'baz'))
        self.assertEqual(nose.test_address(foo_mtc),
                         (me, __name__, 'Foo.bar'))

    def test_tolist(self):
        from nose.util import tolist
        assert tolist('foo') == ['foo']
        assert tolist(['foo', 'bar']) == ['foo', 'bar']
        assert tolist('foo,bar') == ['foo', 'bar']
        self.assertEqual(tolist('.*foo/.*,.1'), ['.*foo/.*', '.1'])

    def test_try_run(self):
        from nose.util import try_run
        import imp

        def bar():
            pass

        def bar_m(mod):
            pass

        class Bar:
            def __call__(self):
                pass

        class Bar_m:
            def __call__(self, mod):
                pass
        
        foo = imp.new_module('foo')
        foo.bar = bar
        foo.bar_m = bar_m
        foo.i_bar = Bar()
        foo.i_bar_m = Bar_m()

        try_run(foo, ('bar',))
        try_run(foo, ('bar_m',))
        try_run(foo, ('i_bar',))
        try_run(foo, ('i_bar_m',))
        
if __name__ == '__main__':
    unittest.main()