namespace Migration.Models;

public class LenModel
{
    public long Id { get; set; }
    public string ModelName { get; set; } = null!;
    public string VersionName { get; set; } = null!;
    public string Description { get; set; } = null!;
    public int MaxResolution { get; set; }
    public int SensorSize { get; set; }
    public int EffectivePixels { get; set; }
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
    public long ImageId { get; set; }
    public long? VideoId { get; set; }
}