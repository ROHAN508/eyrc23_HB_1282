// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from my_custom_msgs:msg/WheelVel.idl
// generated code does not contain a copyright notice
#include "my_custom_msgs/msg/detail/wheel_vel__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
my_custom_msgs__msg__WheelVel__init(my_custom_msgs__msg__WheelVel * msg)
{
  if (!msg) {
    return false;
  }
  // w1
  // w2
  // w3
  // p
  return true;
}

void
my_custom_msgs__msg__WheelVel__fini(my_custom_msgs__msg__WheelVel * msg)
{
  if (!msg) {
    return;
  }
  // w1
  // w2
  // w3
  // p
}

bool
my_custom_msgs__msg__WheelVel__are_equal(const my_custom_msgs__msg__WheelVel * lhs, const my_custom_msgs__msg__WheelVel * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // w1
  if (lhs->w1 != rhs->w1) {
    return false;
  }
  // w2
  if (lhs->w2 != rhs->w2) {
    return false;
  }
  // w3
  if (lhs->w3 != rhs->w3) {
    return false;
  }
  // p
  if (lhs->p != rhs->p) {
    return false;
  }
  return true;
}

bool
my_custom_msgs__msg__WheelVel__copy(
  const my_custom_msgs__msg__WheelVel * input,
  my_custom_msgs__msg__WheelVel * output)
{
  if (!input || !output) {
    return false;
  }
  // w1
  output->w1 = input->w1;
  // w2
  output->w2 = input->w2;
  // w3
  output->w3 = input->w3;
  // p
  output->p = input->p;
  return true;
}

my_custom_msgs__msg__WheelVel *
my_custom_msgs__msg__WheelVel__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_msgs__msg__WheelVel * msg = (my_custom_msgs__msg__WheelVel *)allocator.allocate(sizeof(my_custom_msgs__msg__WheelVel), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(my_custom_msgs__msg__WheelVel));
  bool success = my_custom_msgs__msg__WheelVel__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
my_custom_msgs__msg__WheelVel__destroy(my_custom_msgs__msg__WheelVel * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    my_custom_msgs__msg__WheelVel__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
my_custom_msgs__msg__WheelVel__Sequence__init(my_custom_msgs__msg__WheelVel__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_msgs__msg__WheelVel * data = NULL;

  if (size) {
    data = (my_custom_msgs__msg__WheelVel *)allocator.zero_allocate(size, sizeof(my_custom_msgs__msg__WheelVel), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = my_custom_msgs__msg__WheelVel__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        my_custom_msgs__msg__WheelVel__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
my_custom_msgs__msg__WheelVel__Sequence__fini(my_custom_msgs__msg__WheelVel__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      my_custom_msgs__msg__WheelVel__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

my_custom_msgs__msg__WheelVel__Sequence *
my_custom_msgs__msg__WheelVel__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_msgs__msg__WheelVel__Sequence * array = (my_custom_msgs__msg__WheelVel__Sequence *)allocator.allocate(sizeof(my_custom_msgs__msg__WheelVel__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = my_custom_msgs__msg__WheelVel__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
my_custom_msgs__msg__WheelVel__Sequence__destroy(my_custom_msgs__msg__WheelVel__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    my_custom_msgs__msg__WheelVel__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
my_custom_msgs__msg__WheelVel__Sequence__are_equal(const my_custom_msgs__msg__WheelVel__Sequence * lhs, const my_custom_msgs__msg__WheelVel__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!my_custom_msgs__msg__WheelVel__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
my_custom_msgs__msg__WheelVel__Sequence__copy(
  const my_custom_msgs__msg__WheelVel__Sequence * input,
  my_custom_msgs__msg__WheelVel__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(my_custom_msgs__msg__WheelVel);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    my_custom_msgs__msg__WheelVel * data =
      (my_custom_msgs__msg__WheelVel *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!my_custom_msgs__msg__WheelVel__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          my_custom_msgs__msg__WheelVel__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!my_custom_msgs__msg__WheelVel__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
