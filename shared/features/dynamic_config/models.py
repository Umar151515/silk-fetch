from enum import Enum


class DynamicConfigEnum(Enum):
    TARGET_CHANNEL = "silkroadcargo"
    

    @property
    def key(self) -> str:
        return f"config:{self.name.lower()}"