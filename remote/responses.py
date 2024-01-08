from dataclasses import dataclass

@dataclass
class ItemResponse:
    id: int
    item_code: str
    name: str
    size: int
    unit: str
    created_at: str
    updated_at: str