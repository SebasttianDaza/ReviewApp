namespace Migration.Documents;

public class VideoDocument : Video
{
    public string Credit { get; set; }
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
}