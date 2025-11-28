namespace Migration.Services;

public interface ISqlService
{
    string TableName { get; }

    Task<object?> GetOneAsync(long? id);
}