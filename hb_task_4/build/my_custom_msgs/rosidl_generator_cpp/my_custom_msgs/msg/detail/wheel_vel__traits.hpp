// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from my_custom_msgs:msg/WheelVel.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__TRAITS_HPP_
#define MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "my_custom_msgs/msg/detail/wheel_vel__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace my_custom_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const WheelVel & msg,
  std::ostream & out)
{
  out << "{";
  // member: w1
  {
    out << "w1: ";
    rosidl_generator_traits::value_to_yaml(msg.w1, out);
    out << ", ";
  }

  // member: w2
  {
    out << "w2: ";
    rosidl_generator_traits::value_to_yaml(msg.w2, out);
    out << ", ";
  }

  // member: w3
  {
    out << "w3: ";
    rosidl_generator_traits::value_to_yaml(msg.w3, out);
    out << ", ";
  }

  // member: p
  {
    out << "p: ";
    rosidl_generator_traits::value_to_yaml(msg.p, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const WheelVel & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: w1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w1: ";
    rosidl_generator_traits::value_to_yaml(msg.w1, out);
    out << "\n";
  }

  // member: w2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w2: ";
    rosidl_generator_traits::value_to_yaml(msg.w2, out);
    out << "\n";
  }

  // member: w3
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w3: ";
    rosidl_generator_traits::value_to_yaml(msg.w3, out);
    out << "\n";
  }

  // member: p
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "p: ";
    rosidl_generator_traits::value_to_yaml(msg.p, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const WheelVel & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace my_custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use my_custom_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const my_custom_msgs::msg::WheelVel & msg,
  std::ostream & out, size_t indentation = 0)
{
  my_custom_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use my_custom_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const my_custom_msgs::msg::WheelVel & msg)
{
  return my_custom_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<my_custom_msgs::msg::WheelVel>()
{
  return "my_custom_msgs::msg::WheelVel";
}

template<>
inline const char * name<my_custom_msgs::msg::WheelVel>()
{
  return "my_custom_msgs/msg/WheelVel";
}

template<>
struct has_fixed_size<my_custom_msgs::msg::WheelVel>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<my_custom_msgs::msg::WheelVel>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<my_custom_msgs::msg::WheelVel>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__WHEEL_VEL__TRAITS_HPP_
