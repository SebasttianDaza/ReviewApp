namespace Migration.Models;

public class PublisherDatabaseSettings
{
    public string ConnectionString { get; init; } = null!;
    public string ReviewTableName { get; init; } = null!;
    public string ImageTableName { get; init; } = null!;
    public string VideoTableName { get; init; } = null!;
    public string LenTableName { get; init; } = null!;
    public string CameraTableName { get; init; } = null!;
}