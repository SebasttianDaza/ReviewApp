using Microsoft.Extensions.Options;
using Migration.Models;

namespace Migration.Services;

public class PublisherImageService (IOptions<PublisherDatabaseSettings> settings)
    : SqlService<ImageModel>(settings, settings.Value.ImageTableName)
{
    
}