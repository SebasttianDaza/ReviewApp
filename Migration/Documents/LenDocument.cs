using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Migration.Documents;

public class LenDocument
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }
    
    [BsonElement("model_name")]
    public string ModelName { get; set; }
    
    [BsonElement("version_name")]
    public string VersionName { get; set; }
    
    public string Description { get; set; }
    
    [BsonElement("max_resolution")]
    public int MaxResolution { get; set; }
    [BsonElement("sensor_size")]
    public int SensorSize { get; set; }
    [BsonElement("effective_pixels")]
    public int EffectivePixels { get; set; }
}