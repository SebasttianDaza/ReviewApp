using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Migration.Documents;

public class LenDocument
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }
    
    public string ModelName { get; set; }
    public string VersionName { get; set; }
    
    
}