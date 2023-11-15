from dataclasses import dataclass


# {"id": 2, "folder_name": "Amma", "folder_reference": "10-ObsWjK2CHsFtTJFzPnBwqT6p3SI8bA",
#  "source_type": 1, "knowledge": 24, "created_by": 1, "tenant": 1,
#  "file": {"kind": "drive#file", "mimeType": "audio/mpeg",
#           "id": "1LYRFV74Bv4Lh_YAoLcwn--cH8bzx_Bou", "name": "REC20220330111940.mp3"}
#
#  }

@dataclass
class IngestMessage:
    id: int
    folder_name: str
    folder_reference: str
    source_type: int
    knowledge: int
    created_by: int
    tenant: int
    file: dict
