using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

namespace Migration.Documents;

public class LenDocument: Len, IDocument
{
    [Required(ErrorMessage="Description is required")]
    [BsonElement("description")]
    public string Description { get; set; }
    
    [BsonElement("date_created")]
    [Required(ErrorMessage="Date created is required")]
    public DateTime DateCreated { get; set; }
    
    [BsonElement("date_updated")]
    [Required(ErrorMessage="Date updated is required")]
    public DateTime DateUpdated { get; set; }
    
    
}