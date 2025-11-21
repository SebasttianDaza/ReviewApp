using Azure.Storage.Queues.Models;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using Migration.Services;
using System.Text;
using System.Text.Json;
using Migration.Models;


namespace Migration;

public class Syncronize
{
    private readonly ILogger<Syncronize> _logger;
    private readonly SqlServiceResolver _resolver;

    public Syncronize(ILogger<Syncronize> logger, SqlServiceResolver sqlServiceResolver)
    {
        _logger = logger;
        _resolver = sqlServiceResolver;
    }

    [Function(nameof(Syncronize))]
    public async Task Run([QueueTrigger("publisher", Connection = "AzureWebJobsStorage")] QueueMessage message)
    {
        var messageDecoding = Encoding.UTF8.GetString(Convert.FromBase64String(message.MessageText));
        _logger.LogInformation("C# Queue trigger functio    n processed: {messageText}", messageDecoding);
        MessageModel? messageItem = JsonSerializer.Deserialize<MessageModel>(messageDecoding);
        
        //await _reviewPublisher.TestConnectionAsync();
        var service = _resolver.Resolve(messageItem.TableName);
        var item = await service.GetOneAsync(messageItem.Id);

        if (item is ReviewModel review)
        {
            _logger.LogInformation("{test} {date}", review.Title, review.DateCreated);
        }
    }   
}