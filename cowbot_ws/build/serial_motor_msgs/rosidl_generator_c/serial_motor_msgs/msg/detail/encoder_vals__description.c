// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from serial_motor_msgs:msg/EncoderVals.idl
// generated code does not contain a copyright notice

#include "serial_motor_msgs/msg/detail/encoder_vals__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_serial_motor_msgs
const rosidl_type_hash_t *
serial_motor_msgs__msg__EncoderVals__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x31, 0x27, 0x99, 0xf2, 0x8e, 0x6e, 0x09, 0xc5,
      0x5b, 0x2f, 0x8b, 0xf0, 0x22, 0x0d, 0x63, 0x20,
      0xa5, 0xe2, 0x13, 0xf2, 0x62, 0xf7, 0x95, 0xa7,
      0xec, 0x85, 0x7f, 0x47, 0x18, 0x49, 0x42, 0x40,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char serial_motor_msgs__msg__EncoderVals__TYPE_NAME[] = "serial_motor_msgs/msg/EncoderVals";

// Define type names, field names, and default values
static char serial_motor_msgs__msg__EncoderVals__FIELD_NAME__mot_1_enc_val[] = "mot_1_enc_val";
static char serial_motor_msgs__msg__EncoderVals__FIELD_NAME__mot_2_enc_val[] = "mot_2_enc_val";

static rosidl_runtime_c__type_description__Field serial_motor_msgs__msg__EncoderVals__FIELDS[] = {
  {
    {serial_motor_msgs__msg__EncoderVals__FIELD_NAME__mot_1_enc_val, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {serial_motor_msgs__msg__EncoderVals__FIELD_NAME__mot_2_enc_val, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
serial_motor_msgs__msg__EncoderVals__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {serial_motor_msgs__msg__EncoderVals__TYPE_NAME, 33, 33},
      {serial_motor_msgs__msg__EncoderVals__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "int32 mot_1_enc_val\n"
  "int32 mot_2_enc_val";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
serial_motor_msgs__msg__EncoderVals__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {serial_motor_msgs__msg__EncoderVals__TYPE_NAME, 33, 33},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 40, 40},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
serial_motor_msgs__msg__EncoderVals__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *serial_motor_msgs__msg__EncoderVals__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
