namespace Migration.Documents;

public class ReaderDatabaseSettings
{
    public string ConnectionString { get; init; } = null!;
    public string DatabaseName { get; init; } = null!;
    public string ReviewCollectionName { get; init; } = null!;
    public string ImageCollectionName { get; init; } = null!;
    public string VideoCollectionName { get; init; } = null!;
    public string LenCollectionName { get; init; } = null!;
    public string CameraCollectionName { get; init; } = null!;
}