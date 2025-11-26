namespace Migration.Models;

public class PublisherDatabaseSettings
{
    public string ConnectionString { get; set; } = null!;
    public string ReviewTableName { get; set; } = null!;
    public string ImageTableName { get; set; } = null!;
}