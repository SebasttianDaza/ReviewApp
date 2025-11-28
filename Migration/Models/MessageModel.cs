using System.Text.Json.Serialization;

namespace Migration.Models;

public class MessageModel
{
    [JsonPropertyName("id")]
    public long Id { get; set; }

    [JsonPropertyName("title")] 
    public string Title { get; set; } = null!;
    [JsonPropertyName("table_name")]
    public string TableName { get; set; } = null!;

    [JsonPropertyName("type")] public string Type { get; set; } = null!;
}