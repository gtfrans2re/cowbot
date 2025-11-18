// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from serial_motor_msgs:msg/MotorCommands.idl
// generated code does not contain a copyright notice

#include "serial_motor_msgs/msg/detail/motor_commands__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_serial_motor_msgs
const rosidl_type_hash_t *
serial_motor_msgs__msg__MotorCommands__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x76, 0xb3, 0x8a, 0x80, 0xc8, 0x7c, 0xee, 0xa3,
      0x73, 0xc4, 0xad, 0x7b, 0xa3, 0x11, 0xee, 0x86,
      0xb4, 0xbf, 0x95, 0x6c, 0x8c, 0x4d, 0xe1, 0x28,
      0x28, 0x82, 0x66, 0x94, 0xbe, 0xac, 0x89, 0xd6,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char serial_motor_msgs__msg__MotorCommands__TYPE_NAME[] = "serial_motor_msgs/msg/MotorCommands";

// Define type names, field names, and default values
static char serial_motor_msgs__msg__MotorCommands__FIELD_NAME__is_pwm[] = "is_pwm";
static char serial_motor_msgs__msg__MotorCommands__FIELD_NAME__mot_1_req_rad_sec[] = "mot_1_req_rad_sec";
static char serial_motor_msgs__msg__MotorCommands__FIELD_NAME__mot_2_req_rad_sec[] = "mot_2_req_rad_sec";

static rosidl_runtime_c__type_description__Field serial_motor_msgs__msg__MotorCommands__FIELDS[] = {
  {
    {serial_motor_msgs__msg__MotorCommands__FIELD_NAME__is_pwm, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {serial_motor_msgs__msg__MotorCommands__FIELD_NAME__mot_1_req_rad_sec, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {serial_motor_msgs__msg__MotorCommands__FIELD_NAME__mot_2_req_rad_sec, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
serial_motor_msgs__msg__MotorCommands__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {serial_motor_msgs__msg__MotorCommands__TYPE_NAME, 35, 35},
      {serial_motor_msgs__msg__MotorCommands__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "bool is_pwm\n"
  "float32 mot_1_req_rad_sec \n"
  "float32 mot_2_req_rad_sec ";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
serial_motor_msgs__msg__MotorCommands__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {serial_motor_msgs__msg__MotorCommands__TYPE_NAME, 35, 35},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 66, 66},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
serial_motor_msgs__msg__MotorCommands__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *serial_motor_msgs__msg__MotorCommands__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
