using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Migration.Documents;

public class Video
{
    [BsonId]
    [BsonRepresentation(BsonType.String)]
    public string? Id { get; set; }
    
    [BsonElement("title")]
    public string Title { get; set; }
    [BsonElement("description")]
    public string Description { get; set; }
    [BsonElement("source_id")]
    public string SourceId { get; set; }
    [BsonElement("source")]
    public string Source { get; set; }
}