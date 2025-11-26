using Microsoft.Extensions.Options;
using Migration.Documents;
using MongoDB.Driver;

namespace Migration.Services;

public class MongoService<T> where T : IDocument
{
    protected readonly IMongoCollection<T> Collection;
    
    protected MongoService(
        IOptions<ReaderDatabaseSettings> readerDatabaseSettings,
        string collectionName
    )
    {
        var mongoClient = new MongoClient(
            readerDatabaseSettings.Value.ConnectionString
        );

        var mongoDatabase = mongoClient.GetDatabase(
            readerDatabaseSettings.Value.DatabaseName
        );
        
        Collection = mongoDatabase.GetCollection<T>(collectionName);
    }
    
    public async Task CreateAsync(T item) => await Collection.InsertOneAsync(item);
    
    public async Task<T?> GetAsync(string id) =>
        await Collection.Find(x => x.Id == id).FirstOrDefaultAsync();
}