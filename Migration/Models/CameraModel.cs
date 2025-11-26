namespace Migration.Models;

public class CameraModel
{
    public long Id { get; set; }
    public string ModelName { get; set; } = null!;
    public string Version { get; set; } = null!;
    public string Description { get; set; } = null!;
    public int MaxResolution { get; set; }
    public int SensorSize { get; set; }
    public int EffectivePixels { get; set; }
    public string StorageTypes { get; set; } = null!;
    public string ScreenSize { get; set; } = null!;
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
    public long? ImageId { get; set; }
    public long? VideoId { get; set; }
}