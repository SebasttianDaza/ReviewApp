namespace Migration.Services;

public class SqlServiceResolver
{
    private readonly Dictionary<string, ISqlService> _services;

    public SqlServiceResolver(IEnumerable<ISqlService> services)
    {
        _services = services.ToDictionary(
            s => s.TableName,
            s => s,
            StringComparer.OrdinalIgnoreCase
        );
    }

    public ISqlService Resolve(string tableName)
    {
        if (!_services.TryGetValue(tableName, out var service))
            throw new Exception($"No SQL service for {tableName}");
        
        return service;
    }
}