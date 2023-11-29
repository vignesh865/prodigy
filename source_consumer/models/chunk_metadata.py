from dataclasses import dataclass


@dataclass
class ChunkMetadata:
    tenant_id: int
    cluster_id: int
    data_folder_id: int
    file_name: str
    cloud_url: str
    chunk_id: str
    chunk_group_id: str
    chunk_order: int
