namespace Migration.Models;

public class VideoModel
{
    public long Id { get; set; }
    public string Title { get; set; }
    public string Description { get; set; }
    public string SourceId { get; set; }
    public string Source { get; set; }
    public string Credit { get; set; }
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
}