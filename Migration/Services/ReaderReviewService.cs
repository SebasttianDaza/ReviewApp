using Microsoft.Extensions.Options;
using Migration.Documents;

namespace Migration.Services;

public class ReaderReviewService(IOptions<ReaderDatabaseSettings> settings)
    : MongoService<ReviewDocument>(settings, settings.Value.ReviewCollectionName)
{
    
}