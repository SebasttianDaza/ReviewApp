namespace Migration.Documents;

public class ReaderDatabaseSettings
{
    public string ConnectionString { get; set; } = null!;
    public string DatabaseName { get; set; } = null!;
    public string ReviewCollectionName { get; set; } = null!;
}