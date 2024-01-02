// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_custom_msgs:msg/WheelVel.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__STRUCT_H_
#define MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/WheelVel in the package my_custom_msgs.
typedef struct my_custom_msgs__msg__WheelVel
{
  int32_t w1;
  int32_t w2;
  int32_t w3;
  int32_t p;
} my_custom_msgs__msg__WheelVel;

// Struct for a sequence of my_custom_msgs__msg__WheelVel.
typedef struct my_custom_msgs__msg__WheelVel__Sequence
{
  my_custom_msgs__msg__WheelVel * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_custom_msgs__msg__WheelVel__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__STRUCT_H_
