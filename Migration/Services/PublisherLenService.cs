using Migration.Models;
using Microsoft.Extensions.Options;

namespace Migration.Services;

public class PublisherLenService (IOptions<PublisherDatabaseSettings> settings)
    : SqlService<LenModel>(settings, settings.Value.LenTableName)
{
    
}