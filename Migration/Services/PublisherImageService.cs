using Microsoft.Extensions.Options;
using Migration.Documents;
using Migration.Models;

namespace Migration.Services;

public class PublisherImageService (IOptions<PublisherDatabaseSettings> settings)
    : SqlService<ImageModel>(settings, settings.Value.ImageTableName)
{
    public Image? CreateDocument(ImageModel? image)
    {
        if (image is null) return null;

        return new Image
        {
            Id = image.Id.ToString(),
            Title = image.Title,
            Path = image.Image
        };
    }
}