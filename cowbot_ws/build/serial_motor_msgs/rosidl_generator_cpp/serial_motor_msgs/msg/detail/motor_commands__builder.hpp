// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from serial_motor_msgs:msg/MotorCommands.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "serial_motor_msgs/msg/motor_commands.hpp"


#ifndef SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__BUILDER_HPP_
#define SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "serial_motor_msgs/msg/detail/motor_commands__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace serial_motor_msgs
{

namespace msg
{

namespace builder
{

class Init_MotorCommands_mot_2_req_rad_sec
{
public:
  explicit Init_MotorCommands_mot_2_req_rad_sec(::serial_motor_msgs::msg::MotorCommands & msg)
  : msg_(msg)
  {}
  ::serial_motor_msgs::msg::MotorCommands mot_2_req_rad_sec(::serial_motor_msgs::msg::MotorCommands::_mot_2_req_rad_sec_type arg)
  {
    msg_.mot_2_req_rad_sec = std::move(arg);
    return std::move(msg_);
  }

private:
  ::serial_motor_msgs::msg::MotorCommands msg_;
};

class Init_MotorCommands_mot_1_req_rad_sec
{
public:
  explicit Init_MotorCommands_mot_1_req_rad_sec(::serial_motor_msgs::msg::MotorCommands & msg)
  : msg_(msg)
  {}
  Init_MotorCommands_mot_2_req_rad_sec mot_1_req_rad_sec(::serial_motor_msgs::msg::MotorCommands::_mot_1_req_rad_sec_type arg)
  {
    msg_.mot_1_req_rad_sec = std::move(arg);
    return Init_MotorCommands_mot_2_req_rad_sec(msg_);
  }

private:
  ::serial_motor_msgs::msg::MotorCommands msg_;
};

class Init_MotorCommands_is_pwm
{
public:
  Init_MotorCommands_is_pwm()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorCommands_mot_1_req_rad_sec is_pwm(::serial_motor_msgs::msg::MotorCommands::_is_pwm_type arg)
  {
    msg_.is_pwm = std::move(arg);
    return Init_MotorCommands_mot_1_req_rad_sec(msg_);
  }

private:
  ::serial_motor_msgs::msg::MotorCommands msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::serial_motor_msgs::msg::MotorCommands>()
{
  return serial_motor_msgs::msg::builder::Init_MotorCommands_is_pwm();
}

}  // namespace serial_motor_msgs

#endif  // SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__BUILDER_HPP_
