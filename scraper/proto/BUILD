package(default_visibility = ["//visibility:public"])

load("@rules_proto//proto:defs.bzl", "proto_library")

proto_library(
    name = "concert_event_proto",
    srcs = ["concert_event.proto"],
    deps = ["@com_google_protobuf//:timestamp_proto"],
)

load("@rules_proto_grpc//python:defs.bzl", "py_proto_library")

py_proto_library(
    name = "py_concert_event_proto",
    protos = [":concert_event_proto"],
)
