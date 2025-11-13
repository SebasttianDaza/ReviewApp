using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Migration.Documents;

public class Image
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }
    
    public string Title { get; set; }
    public string Path { get; set; }
}