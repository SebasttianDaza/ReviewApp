from redis import StrictRedis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.index_definition import IndexDefinition, IndexType

class CacheRepository:
    def __init__(self, master_conn: StrictRedis, replica_conn: StrictRedis):
        self.master = master_conn
        self.replica = replica_conn

    #def build_key(self, prefix: str, key_id):

    def create_search_index(self, index_name: str, prefix: str ):
        schema = (
            TextField("$.title", as_name="title"),
            TextField("$.subtitle", as_name="subtitle"),
            TextField("$.body", as_name="body"),
            TextField("$.date_created", as_name="date_created"),
            TextField("$.date_updated", as_name="date_updated"),
            TextField("$.video.title", as_name="video_title"),
            TextField("$.video.description", as_name="video_description"),
            TextField("$.video.source_id", as_name="video_source_id"),
            TextField("$.video.source", as_name="video_source"),
            TextField("$.image.title", as_name="image_title"),
            TextField("$.image.path", as_name="image_path"),
            TextField("$.len.model_name", as_name="len_name"),
            TextField("$.len.version_name", as_name="len_version_name"),
            TextField("$.len.description", as_name="len_description"),
            NumericField("$.len.max_resolution", as_name="len_max_resolution"),
            NumericField("$.len.effective_pixels", as_name="len_effective_pixels"),
            TextField("$.camera.model_name", as_name="camera_name"),
            TextField("$.camera.version", as_name="camera_version"),
            NumericField("$.camera.sensor_size", as_name="camera_sensor_size"),
            NumericField("$.camera.effective_pixels", as_name="camera_effective_pixels"),
            TextField("$.camera.storage_types", as_name="camera_storage_types"),
            TextField("$.camera.screen_size", as_name="camera_screen_size"),
        )

        try:
            self.master.ft(index_name).create_index(
                schema,
                definition=IndexDefinition(prefix=[f"idx:{prefix}"], index_type=IndexType.JSON)
            )

            print(f"Índex '{index_name}' created/updated successfully with prefix doc:{prefix}:")
        except Exception as e:
            print(e)
            # Captura si el índice ya existe, lo cual es normal en la inicialización
            if "Index already exists" not in str(e):
                raise e
