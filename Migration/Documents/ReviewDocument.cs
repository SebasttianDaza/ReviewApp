using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

namespace Migration.Documents;

public class ReviewDocument: IDocument
{   
    [Required]
    [BsonId]
    [BsonRepresentation(BsonType.String)]
    public string? Id { get; set; }
    
    [Required(ErrorMessage= "Title of review is required")]
    [BsonElement("title")]
    public string Title { get; set; }
    
    [Required(ErrorMessage= "Subtitle of review is required")]
    [BsonElement("subtitle")]
    public string Subtitle { get; set; }
    
    [Required(ErrorMessage= "Body of review is required")]
    [BsonElement("body")]
    public string Body { get; set; }
    
    [BsonElement("date_created")]
    [Required(ErrorMessage = "Date created is required")]
    public DateTime DateCreated { get; set; }
    
    [BsonElement("date_updated")]
    [Required(ErrorMessage = "Date updated is required")]
    public DateTime DateUpdated { get; set; }

    [BsonElement("video")]
    public Video? Video { get; set; }
    [BsonElement("image")]
    public Image? Image { get; set; }
    [BsonElment("len")]
    public LenDocument? Len { get; set; }
}