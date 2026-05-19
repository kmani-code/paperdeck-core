from dataclasses import dataclass, field
from typing import Any, List, Optional

import marshmallow_dataclass
from dataclasses_json import dataclass_json


@dataclass
class BlueprintRequest:
    name:        str
    exam:        str
    duration:    str
    total_marks: int
    neg_marking: str
    sections:    List[Any] = field(default_factory=list)
    id:          Optional[int] = None


blueprint_req_schema = marshmallow_dataclass.class_schema(BlueprintRequest)()


@dataclass_json
@dataclass
class BlueprintResponse:
    id:          int
    name:        str
    exam:        str
    duration:    str
    total_marks: int
    neg_marking: str
    sections:    List[Any]
    created_at:  str
