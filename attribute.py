##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Attribute Annotations implementation 

$Id$
"""
__docformat__ = 'restructuredtext'

from UserDict import DictMixin

from BTrees.OOBTree import OOBTree

from zope.interface import implements

from interfaces import IAnnotations, IAttributeAnnotatable


class AttributeAnnotations(DictMixin):
    """Store annotations in the `__annotations__` attribute on a
       `IAttributeAnnotatable` object.
    """
    implements(IAnnotations)
    __used_for__ = IAttributeAnnotatable

    def __init__(self, obj):
        self.obj = obj        

    def get(self, key, default=None):
        """See zope.app.annotation.interfaces.IAnnotations"""
        annotations = getattr(self.obj, '__annotations__', None)
        if not annotations:
            return default

        return annotations.get(key, default)

    def __getitem__(self, key):
        annotations = getattr(self.obj, '__annotations__', None)
        if annotations is None:
            raise KeyError, key

        return annotations[key]
        
    def keys(self):
        annotations = getattr(self.obj, '__annotations__', None)
        if annotations is None:
            return []

        return annotations.keys()
    
    def __setitem__(self, key, value):
        """See zope.app.annotation.interfaces.IAnnotations"""
        
        try:
            annotations = self.obj.__annotations__
        except AttributeError:
            annotations = self.obj.__annotations__ = OOBTree()

        annotations[key] = value

    def __delitem__(self, key):
        """See zope.app.interfaces.annotation.IAnnotations"""
        try:
            annotation = self.obj.__annotations__
        except AttributeError:
            raise KeyError, key

        del annotation[key]
