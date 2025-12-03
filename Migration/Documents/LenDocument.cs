using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

namespace Migration.Documents;

public class LenDocument: IDocument
{
    [Required]
    [BsonId]
    [BsonRepresentation(BsonType.String)]
    public string? Id { get; set; }
    
    [Required(ErrorMessage="Model name is required")]
    [BsonElement("model_name")]
    public string ModelName { get; set; }
    
    [Required(ErrorMessage="Version name is required")]
    [BsonElement("version_name")]
    public string VersionName { get; set; }
    
    [Required(ErrorMessage="Description is required")]
    [BsonElement("description")]
    public string Description { get; set; }
    
    [Required(ErrorMessage="Max resolution is required")]
    [BsonElement("max_resolution")]
    public int MaxResolution { get; set; }
    
    [Required(ErrorMessage="Sensor size is required")]
    [BsonElement("sensor_size")]
    public int SensorSize { get; set; }
    
    [Required(ErrorMessage="Effective pixels is required")]
    [BsonElement("effective_pixels")]
    public int EffectivePixels { get; set; }
    
    [BsonElement("date_created")]
    [Required(ErrorMessage="Date created is required")]
    public DateTime DateCreated { get; set; }
    
    [BsonElement("date_updated")]
    [Required(ErrorMessage="Date updated is required")]
    public DateTime DateUpdated { get; set; }
    
    [BsonElement("video")]
    public Video? Video { get; set; }
    
    [Required(ErrorMessage="Image is required")]
    [BsonElement("image")]
    public Image Image { get; set; }
}