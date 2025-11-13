namespace Migration.Documents;

public class ImageDocument: Image
{
    public string Description { get; set; }
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
}