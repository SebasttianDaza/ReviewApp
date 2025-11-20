using Microsoft.Extensions.Options;
using Migration.Models;

namespace Migration.Services;

public class ReviewPublisherService (IOptions<PublisherDatabaseSettings> settings)
    : SqlService<ReviewModel>(settings, settings.Value.ReviewTableName)
{
    
}