// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from serial_motor_msgs:msg/MotorCommands.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "serial_motor_msgs/msg/motor_commands.h"


#ifndef SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__STRUCT_H_
#define SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/MotorCommands in the package serial_motor_msgs.
typedef struct serial_motor_msgs__msg__MotorCommands
{
  bool is_pwm;
  float mot_1_req_rad_sec;
  float mot_2_req_rad_sec;
} serial_motor_msgs__msg__MotorCommands;

// Struct for a sequence of serial_motor_msgs__msg__MotorCommands.
typedef struct serial_motor_msgs__msg__MotorCommands__Sequence
{
  serial_motor_msgs__msg__MotorCommands * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} serial_motor_msgs__msg__MotorCommands__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SERIAL_MOTOR_MSGS__MSG__DETAIL__MOTOR_COMMANDS__STRUCT_H_
