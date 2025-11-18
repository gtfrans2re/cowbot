// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from serial_motor_msgs:msg/MotorCommands.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "serial_motor_msgs/msg/motor_commands.hpp"


#ifndef SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__STRUCT_HPP_
#define SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__serial_motor_msgs__msg__MotorCommands __attribute__((deprecated))
#else
# define DEPRECATED__serial_motor_msgs__msg__MotorCommands __declspec(deprecated)
#endif

namespace serial_motor_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotorCommands_
{
  using Type = MotorCommands_<ContainerAllocator>;

  explicit MotorCommands_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_pwm = false;
      this->mot_1_req_rad_sec = 0.0f;
      this->mot_2_req_rad_sec = 0.0f;
    }
  }

  explicit MotorCommands_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_pwm = false;
      this->mot_1_req_rad_sec = 0.0f;
      this->mot_2_req_rad_sec = 0.0f;
    }
  }

  // field types and members
  using _is_pwm_type =
    bool;
  _is_pwm_type is_pwm;
  using _mot_1_req_rad_sec_type =
    float;
  _mot_1_req_rad_sec_type mot_1_req_rad_sec;
  using _mot_2_req_rad_sec_type =
    float;
  _mot_2_req_rad_sec_type mot_2_req_rad_sec;

  // setters for named parameter idiom
  Type & set__is_pwm(
    const bool & _arg)
  {
    this->is_pwm = _arg;
    return *this;
  }
  Type & set__mot_1_req_rad_sec(
    const float & _arg)
  {
    this->mot_1_req_rad_sec = _arg;
    return *this;
  }
  Type & set__mot_2_req_rad_sec(
    const float & _arg)
  {
    this->mot_2_req_rad_sec = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    serial_motor_msgs::msg::MotorCommands_<ContainerAllocator> *;
  using ConstRawPtr =
    const serial_motor_msgs::msg::MotorCommands_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<serial_motor_msgs::msg::MotorCommands_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<serial_motor_msgs::msg::MotorCommands_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      serial_motor_msgs::msg::MotorCommands_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<serial_motor_msgs::msg::MotorCommands_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      serial_motor_msgs::msg::MotorCommands_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<serial_motor_msgs::msg::MotorCommands_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<serial_motor_msgs::msg::MotorCommands_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<serial_motor_msgs::msg::MotorCommands_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__serial_motor_msgs__msg__MotorCommands
    std::shared_ptr<serial_motor_msgs::msg::MotorCommands_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__serial_motor_msgs__msg__MotorCommands
    std::shared_ptr<serial_motor_msgs::msg::MotorCommands_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorCommands_ & other) const
  {
    if (this->is_pwm != other.is_pwm) {
      return false;
    }
    if (this->mot_1_req_rad_sec != other.mot_1_req_rad_sec) {
      return false;
    }
    if (this->mot_2_req_rad_sec != other.mot_2_req_rad_sec) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorCommands_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorCommands_

// alias to use template instance with default allocator
using MotorCommands =
  serial_motor_msgs::msg::MotorCommands_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace serial_motor_msgs

#endif  // SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__STRUCT_HPP_
