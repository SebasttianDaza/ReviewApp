using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Migration.Documents;

public class Image
{
    [BsonId]
    [BsonRepresentation(BsonType.String)]
    public string? Id { get; set; }
    
    [BsonElement("title")]
    public string Title { get; set; }
    [BsonElement("path")]
    public string Path { get; set; }
}