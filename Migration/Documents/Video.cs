using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Migration.Documents;

public class Video
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }
    
    public string Title { get; set; }
    public string Description { get; set; }
    public string SourceId { get; set; }
    public string Source { get; set; }
}