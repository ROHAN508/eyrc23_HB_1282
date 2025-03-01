# generated from rosidl_generator_py/resource/_idl.py.em
# with input from my_custom_msgs:msg/WheelVel.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_WheelVel(type):
    """Metaclass of message 'WheelVel'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('my_custom_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'my_custom_msgs.msg.WheelVel')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__wheel_vel
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__wheel_vel
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__wheel_vel
            cls._TYPE_SUPPORT = module.type_support_msg__msg__wheel_vel
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__wheel_vel

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class WheelVel(metaclass=Metaclass_WheelVel):
    """Message class 'WheelVel'."""

    __slots__ = [
        '_w1',
        '_w2',
        '_w3',
        '_p',
    ]

    _fields_and_field_types = {
        'w1': 'int32',
        'w2': 'int32',
        'w3': 'int32',
        'p': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.w1 = kwargs.get('w1', int())
        self.w2 = kwargs.get('w2', int())
        self.w3 = kwargs.get('w3', int())
        self.p = kwargs.get('p', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.w1 != other.w1:
            return False
        if self.w2 != other.w2:
            return False
        if self.w3 != other.w3:
            return False
        if self.p != other.p:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def w1(self):
        """Message field 'w1'."""
        return self._w1

    @w1.setter
    def w1(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'w1' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'w1' field must be an integer in [-2147483648, 2147483647]"
        self._w1 = value

    @builtins.property
    def w2(self):
        """Message field 'w2'."""
        return self._w2

    @w2.setter
    def w2(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'w2' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'w2' field must be an integer in [-2147483648, 2147483647]"
        self._w2 = value

    @builtins.property
    def w3(self):
        """Message field 'w3'."""
        return self._w3

    @w3.setter
    def w3(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'w3' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'w3' field must be an integer in [-2147483648, 2147483647]"
        self._w3 = value

    @builtins.property
    def p(self):
        """Message field 'p'."""
        return self._p

    @p.setter
    def p(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'p' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'p' field must be an integer in [-2147483648, 2147483647]"
        self._p = value
