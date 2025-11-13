using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.ComponentModel.DataAnnotations;

namespace Migration.Documents;

public class ReviewDocument
{   
    [Required]
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string? Id { get; set; }
    
    [Required(ErrorMessage= "Title of review is required")]
    public string Title { get; set; }
    
    [Required(ErrorMessage= "Subtitle of review is required")]
    public string SubTitle { get; set; }
    
    [Required(ErrorMessage= "Body of review is required")]
    public string Body { get; set; }
    
    [BsonElement("date_created")]
    [Required(ErrorMessage = "Date created is required")]
    public DateTime DateCreated { get; set; }
    
    [BsonElement("date_updated")]
    [Required(ErrorMessage = "Date updated is required")]
    public DateTime DateUpdated { get; set; }

    public Video Video { get; set; } = null!;
    public Image Image { get; set; } = null!;
}