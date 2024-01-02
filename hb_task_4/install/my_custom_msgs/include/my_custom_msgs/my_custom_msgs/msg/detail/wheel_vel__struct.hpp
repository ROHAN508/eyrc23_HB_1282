// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_custom_msgs:msg/WheelVel.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__STRUCT_HPP_
#define MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_custom_msgs__msg__WheelVel __attribute__((deprecated))
#else
# define DEPRECATED__my_custom_msgs__msg__WheelVel __declspec(deprecated)
#endif

namespace my_custom_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct WheelVel_
{
  using Type = WheelVel_<ContainerAllocator>;

  explicit WheelVel_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->w1 = 0l;
      this->w2 = 0l;
      this->w3 = 0l;
      this->p = 0l;
    }
  }

  explicit WheelVel_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->w1 = 0l;
      this->w2 = 0l;
      this->w3 = 0l;
      this->p = 0l;
    }
  }

  // field types and members
  using _w1_type =
    int32_t;
  _w1_type w1;
  using _w2_type =
    int32_t;
  _w2_type w2;
  using _w3_type =
    int32_t;
  _w3_type w3;
  using _p_type =
    int32_t;
  _p_type p;

  // setters for named parameter idiom
  Type & set__w1(
    const int32_t & _arg)
  {
    this->w1 = _arg;
    return *this;
  }
  Type & set__w2(
    const int32_t & _arg)
  {
    this->w2 = _arg;
    return *this;
  }
  Type & set__w3(
    const int32_t & _arg)
  {
    this->w3 = _arg;
    return *this;
  }
  Type & set__p(
    const int32_t & _arg)
  {
    this->p = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_custom_msgs::msg::WheelVel_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_custom_msgs::msg::WheelVel_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_custom_msgs::msg::WheelVel_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_custom_msgs::msg::WheelVel_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_custom_msgs::msg::WheelVel_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_custom_msgs::msg::WheelVel_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_custom_msgs::msg::WheelVel_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_custom_msgs::msg::WheelVel_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_custom_msgs::msg::WheelVel_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_custom_msgs::msg::WheelVel_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_custom_msgs__msg__WheelVel
    std::shared_ptr<my_custom_msgs::msg::WheelVel_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_custom_msgs__msg__WheelVel
    std::shared_ptr<my_custom_msgs::msg::WheelVel_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const WheelVel_ & other) const
  {
    if (this->w1 != other.w1) {
      return false;
    }
    if (this->w2 != other.w2) {
      return false;
    }
    if (this->w3 != other.w3) {
      return false;
    }
    if (this->p != other.p) {
      return false;
    }
    return true;
  }
  bool operator!=(const WheelVel_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct WheelVel_

// alias to use template instance with default allocator
using WheelVel =
  my_custom_msgs::msg::WheelVel_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace my_custom_msgs

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__STRUCT_HPP_
