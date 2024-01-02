// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_custom_msgs:msg/WheelVel.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__BUILDER_HPP_
#define MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_custom_msgs/msg/detail/wheel_vel__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_custom_msgs
{

namespace msg
{

namespace builder
{

class Init_WheelVel_p
{
public:
  explicit Init_WheelVel_p(::my_custom_msgs::msg::WheelVel & msg)
  : msg_(msg)
  {}
  ::my_custom_msgs::msg::WheelVel p(::my_custom_msgs::msg::WheelVel::_p_type arg)
  {
    msg_.p = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_custom_msgs::msg::WheelVel msg_;
};

class Init_WheelVel_w3
{
public:
  explicit Init_WheelVel_w3(::my_custom_msgs::msg::WheelVel & msg)
  : msg_(msg)
  {}
  Init_WheelVel_p w3(::my_custom_msgs::msg::WheelVel::_w3_type arg)
  {
    msg_.w3 = std::move(arg);
    return Init_WheelVel_p(msg_);
  }

private:
  ::my_custom_msgs::msg::WheelVel msg_;
};

class Init_WheelVel_w2
{
public:
  explicit Init_WheelVel_w2(::my_custom_msgs::msg::WheelVel & msg)
  : msg_(msg)
  {}
  Init_WheelVel_w3 w2(::my_custom_msgs::msg::WheelVel::_w2_type arg)
  {
    msg_.w2 = std::move(arg);
    return Init_WheelVel_w3(msg_);
  }

private:
  ::my_custom_msgs::msg::WheelVel msg_;
};

class Init_WheelVel_w1
{
public:
  Init_WheelVel_w1()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_WheelVel_w2 w1(::my_custom_msgs::msg::WheelVel::_w1_type arg)
  {
    msg_.w1 = std::move(arg);
    return Init_WheelVel_w2(msg_);
  }

private:
  ::my_custom_msgs::msg::WheelVel msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_custom_msgs::msg::WheelVel>()
{
  return my_custom_msgs::msg::builder::Init_WheelVel_w1();
}

}  // namespace my_custom_msgs

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__BUILDER_HPP_
