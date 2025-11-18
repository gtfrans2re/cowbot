// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from serial_motor_msgs:msg/MotorVels.idl
// generated code does not contain a copyright notice

#include "serial_motor_msgs/msg/detail/motor_vels__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_serial_motor_msgs
const rosidl_type_hash_t *
serial_motor_msgs__msg__MotorVels__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x8f, 0x91, 0x61, 0xec, 0x9f, 0x64, 0xd0, 0xce,
      0xe6, 0x74, 0x21, 0x31, 0xa5, 0xb6, 0xc2, 0x0c,
      0x57, 0xda, 0xed, 0xd1, 0x4d, 0x0a, 0xea, 0x39,
      0x52, 0xf1, 0xe3, 0x45, 0xb4, 0x4a, 0xc2, 0xb4,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char serial_motor_msgs__msg__MotorVels__TYPE_NAME[] = "serial_motor_msgs/msg/MotorVels";

// Define type names, field names, and default values
static char serial_motor_msgs__msg__MotorVels__FIELD_NAME__mot_1_rad_sec[] = "mot_1_rad_sec";
static char serial_motor_msgs__msg__MotorVels__FIELD_NAME__mot_2_rad_sec[] = "mot_2_rad_sec";

static rosidl_runtime_c__type_description__Field serial_motor_msgs__msg__MotorVels__FIELDS[] = {
  {
    {serial_motor_msgs__msg__MotorVels__FIELD_NAME__mot_1_rad_sec, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {serial_motor_msgs__msg__MotorVels__FIELD_NAME__mot_2_rad_sec, 13, 13},
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
serial_motor_msgs__msg__MotorVels__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {serial_motor_msgs__msg__MotorVels__TYPE_NAME, 31, 31},
      {serial_motor_msgs__msg__MotorVels__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 mot_1_rad_sec\n"
  "float32 mot_2_rad_sec";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
serial_motor_msgs__msg__MotorVels__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {serial_motor_msgs__msg__MotorVels__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 44, 44},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
serial_motor_msgs__msg__MotorVels__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *serial_motor_msgs__msg__MotorVels__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
