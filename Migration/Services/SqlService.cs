using System.Collections.Concurrent;
using System.Data.Common;
using Migration.Models;
using System.Reflection;
using Microsoft.Extensions.Options;
using MySql.Data.MySqlClient;
using System;

namespace Migration.Services;

public class SqlService<T> : ISqlService where T : new()
{
    private readonly string _connectionString;
    private readonly string _tableName;
    public string TableName => _tableName;
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

    public async Task<object?> GetOneAsync(long? id)
    {
        if (id is null) return null;
        return await GetOneTypeAsync(id);
    }

    private async Task<T?> GetOneTypeAsync(long? id)
    {
        var query = $"SELECT * FROM {_tableName} WHERE id = @Id";
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
            var sqlName = ToSnakeCase(prop.Name);
            if (!columnNames.Contains(sqlName)) continue;
            var value = reader[sqlName];
            if (value == DBNull.Value) continue;
            prop.SetValue(entity, value);
        }
        
        return entity;
    }

    private static string ToSnakeCase(string input)
    {
        return string.Concat(
            input.Select((x, i) => 
                i > 0 && char.IsUpper(x)
                ? $"_{x}"
                : x.ToString()
            )
        ).ToLower();
    }

    public async Task TestConnectionAsync()
    {
        var query = $"SELECT COUNT(*) FROM {_tableName}";
        await using var conn = CreateConnection();
        await conn.OpenAsync();
        Console.WriteLine("Connected OK mysql");
        
        await using var cmd = new MySqlCommand(query, conn);
        Console.WriteLine(Convert.ToInt32(await cmd.ExecuteScalarAsync()));
    }
}