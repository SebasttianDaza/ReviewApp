using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Migration.Documents;

public class Image
{
    [BsonElement("title")]
    public string Title { get; set; }
    [BsonElement("path")]
    public string Path { get; set; }
}