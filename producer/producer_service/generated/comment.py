# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: comment.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


@dataclass
class Comment(betterproto.Message):
    comment_id: str = betterproto.string_field(1)
    content: str = betterproto.string_field(2)
