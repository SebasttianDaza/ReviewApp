namespace Migration.Models;

public class ReviewModel
{
    public long Id { get; set; }
    public string Title { get; set; }
    public string SubTitle { get; set; }
    public string Body { get; set; }
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
    public long CameraId { get; set; }
    public long ImageId { get; set; }
    public long LenId { get; set; }
    public long VideoId { get; set; }
}