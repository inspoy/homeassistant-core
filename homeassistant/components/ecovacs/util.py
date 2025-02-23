"""Ecovacs util functions."""

from __future__ import annotations

from enum import Enum
import random
import string
from typing import TYPE_CHECKING

from deebot_client.capabilities import Capabilities

from homeassistant.core import callback

from .entity import (
    EcovacsCapabilityEntityDescription,
    EcovacsDescriptionEntity,
    EcovacsEntity,
)

if TYPE_CHECKING:
    from .controller import EcovacsController


def get_client_device_id() -> str:
    """Get client device id."""
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
    )


def get_supported_entitites(
    controller: EcovacsController,
    entity_class: type[EcovacsDescriptionEntity],
    descriptions: tuple[EcovacsCapabilityEntityDescription, ...],
) -> list[EcovacsEntity]:
    """Return all supported entities for all devices."""
    return [
        entity_class(device, capability, description)
        for device in controller.devices(Capabilities)
        for description in descriptions
        if isinstance(device.capabilities, description.device_capabilities)
        if (capability := description.capability_fn(device.capabilities))
    ]


@callback
def get_name_key(enum: Enum) -> str:
    """Return the lower case name of the enum."""
    return enum.name.lower()
