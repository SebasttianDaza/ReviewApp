using System.Collections.Concurrent;
using System.Data.Common;
using Migration.Models;
using System.Reflection;
using Microsoft.Extensions.Options;
using MySql.Data.MySqlClient;

namespace Migration.Services;

public class SqlService<T> where T : new()
{
    private readonly string _connectionString;
    private readonly string _tableName;
    private static readonly ConcurrentDictionary<Type, PropertyInfo[]> _propsCache = new();

    protected SqlService(
        IOptions<PublisherDatabaseSettings> publisherDatabaseSettings,
        string tableName
    )
    {   
       _connectionString = publisherDatabaseSettings.Value.ConnectionString;
       _tableName = tableName;
    }
    
    private MySqlConnection CreateConnection() => new MySqlConnection(_connectionString);

    public async Task<T?> GetOneAsync(int id)
    {
        var query = $"SELECT * FROM `{_tableName}` WHERE id = @Id";
        await using var connection = CreateConnection();
        await using var cmd = new MySqlCommand(query, connection);
        cmd.Parameters.AddWithValue("@Id", id);

        await connection.OpenAsync();
        await using var reader = await cmd.ExecuteReaderAsync();
        return await reader.ReadAsync() ? Map(reader): default;
    }

    private T Map(DbDataReader reader)
    {
        var entity = new T();
        var props = _propsCache.GetOrAdd(typeof(T), t => t.GetProperties(BindingFlags.Public | BindingFlags.Instance));
        var columnNames = Enumerable.Range(0, reader.FieldCount).Select(reader.GetName).ToHashSet(
            StringComparer.OrdinalIgnoreCase    
        );

        foreach (var prop in props)
        {
            var sqlName = prop.Name;
            if (!columnNames.Contains(sqlName)) continue;
            var value = reader[sqlName];
            if (value == DBNull.Value) continue;
            prop.SetValue(entity, value);
        }
        
        return entity;
    }
}