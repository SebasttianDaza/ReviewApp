namespace Migration.Documents;

public interface IDocument
{
    string? Id { get; set; }
    DateTime DateCreated { get; set; }
    DateTime DateUpdated { get; set; }
}