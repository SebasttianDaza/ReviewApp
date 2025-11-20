using System.Text.Json.Serialization;

namespace Migration.Models;

public class MessageModel
{
    [JsonPropertyName("id")]
    public long Id { get; set; }
    [JsonPropertyName("title")]
    public string Title { get; set; }
    [JsonPropertyName("table_name")]
    public string TableName { get; set; }
    [JsonPropertyName("type")]
    public string Type { get; set; }
}