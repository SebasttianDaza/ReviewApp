using Microsoft.Extensions.Options;
using Migration.Documents;

namespace Migration.Services;

public class ReviewReaderService(IOptions<ReaderDatabaseSettings> settings)
    : MongoService<ReviewDocument>(settings, settings.Value.ReviewCollectionName)
{
    
}