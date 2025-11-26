using Migration.Models;
using Microsoft.Extensions.Options;

namespace Migration.Services;

public class PublisherCameraService (IOptions<PublisherDatabaseSettings> settings)
    : SqlService<CameraModel>(settings, settings.Value.LenTableName)
{
    
}