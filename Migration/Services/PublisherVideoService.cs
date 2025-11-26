using Migration.Models;
using Microsoft.Extensions.Options;

namespace Migration.Services;

public class PublisherVideoService(IOptions<PublisherDatabaseSettings> settings)
    : SqlService<VideoModel>(settings, settings.Value.VideoTableName)
{
    
}