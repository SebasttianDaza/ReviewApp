namespace Migration.Models;

public class ReviewModel
{
    public long Id { get; set; }
    public string Title { get; set; } = null!;
    public string Subtitle { get; set; } = null!;
    public string Body { get; set; } = null!;
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
    public long? CameraId { get; set; }
    public long? ImageId { get; set; }
    public long? LenId { get; set; }
    public long? VideoId { get; set; }
}