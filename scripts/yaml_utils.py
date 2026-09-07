"""YAML loading with the restrictions used by the Ruby verifier.

``yaml.safe_load`` is close to Psych's ``YAML.safe_load`` but differs in two
ways that matter for repository metadata: PyYAML resolves timestamps to
``date``/``datetime`` objects, accepts aliases by default, and constructs YAML
sets as Python ``set`` objects.  The maintainer scripts only consume simple,
portable YAML, so those constructs are rejected here along with PyYAML's
normal refusal of custom Python tags.
"""

from __future__ import annotations

from typing import Any

import yaml
from yaml.constructor import ConstructorError
from yaml.events import AliasEvent


class StrictSafeLoader(yaml.SafeLoader):
    """SafeLoader variant matching ``YAML.safe_load(..., aliases: false)``."""

    def compose_node(self, parent: Any, index: Any) -> Any:
        if self.check_event(AliasEvent):
            event = self.get_event()
            raise ConstructorError(
                None,
                None,
                "aliases are not permitted",
                event.start_mark,
            )
        return super().compose_node(parent, index)


def _reject_timestamp(loader: StrictSafeLoader, node: yaml.Node) -> Any:
    del loader
    raise ConstructorError(
        "while constructing a YAML value",
        node.start_mark,
        "date/time values are not permitted",
        node.start_mark,
    )


StrictSafeLoader.add_constructor("tag:yaml.org,2002:timestamp", _reject_timestamp)


def _reject_set(loader: StrictSafeLoader, node: yaml.Node) -> Any:
    del loader
    raise ConstructorError(
        "while constructing a YAML value",
        node.start_mark,
        "set values are not permitted",
        node.start_mark,
    )


# Psych represents ``!!set`` as ``Psych::Set``, which is not in the empty
# permitted class list used by the Ruby scripts.
StrictSafeLoader.add_constructor("tag:yaml.org,2002:set", _reject_set)


def safe_load(source: str) -> Any:
    """Parse portable YAML and reject aliases, timestamps, and custom tags."""

    return yaml.load(source, Loader=StrictSafeLoader)


__all__ = ["StrictSafeLoader", "safe_load"]
