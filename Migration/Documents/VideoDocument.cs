using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;


namespace Migration.Documents;

public class VideoDocument : Video, IDocument
{
    [BsonId]
    [BsonRepresentation(BsonType.String)]
    public string? Id { get; set; }
    public string Credit { get; set; }
    public DateTime DateCreated { get; set; }
    public DateTime DateUpdated { get; set; }
}