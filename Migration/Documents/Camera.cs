using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

namespace Migration.Documents;

public class Camera
{
    [Required]
    [BsonId]
    [BsonRepresentation(BsonType.String)]
    public string? Id { get; set; }

    [Required(ErrorMessage = "Model name is required")]
    [BsonElement("model_name")]
    public string ModelName { get; set; } = null!;

    [Required(ErrorMessage = "Version is required")]
    [BsonElement("version")]
    public string Version { get; set; } = null!;
    
    [Required(ErrorMessage="Max resolution is required")]
    [BsonElement("max_resolution")]
    public int MaxResolution { get; set; }
    
    [Required(ErrorMessage="Sensor size is required")]
    [BsonElement("sensor_size")]
    public int SensorSize { get; set; }
    
    [Required(ErrorMessage="Effective pixels is required")]
    [BsonElement("effective_pixels")]
    public int EffectivePixels { get; set; }

    [Required(ErrorMessage = "Storage types is required")]
    [BsonElement("storage_types")]
    public string StorageTypes { get; set; } = null!;

    [Required(ErrorMessage = "Screen size is required")]
    [BsonElement("screen_size")]
    public string ScreenSize { get; set; } = null!;
    
    [BsonElement("video")]
    public Video? Video { get; set; }
    
    [Required(ErrorMessage="Image is required")]
    [BsonElement("image")]
    public Image? Image { get; set; }
}