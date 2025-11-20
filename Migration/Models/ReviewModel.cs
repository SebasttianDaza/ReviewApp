namespace Migration.Models;

public class ReviewModel
{
    public int Id { get; set; }
    public string Title { get; set; }
    public string SubTitle { get; set; }
    public string Body { get; set; }
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
    public int CameraId { get; set; }
    public int ImageId { get; set; }
    public int LenId { get; set; }
    public int VideoId { get; set; }
}