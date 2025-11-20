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
    private readonly ReviewPublisherService _reviewPublisher;

    public Syncronize(ILogger<Syncronize> logger, ReviewReaderService reviewReaderService, ReviewPublisherService reviewPublisherService)
    {
        _logger = logger;
        _reviewPublisher = reviewPublisherService;
    }

    [Function(nameof(Syncronize))]
    public async Task Run([QueueTrigger("publisher", Connection = "AzureWebJobsStorage")] QueueMessage message)
    {
        var messageDecoding = Encoding.UTF8.GetString(Convert.FromBase64String(message.MessageText));
        _logger.LogInformation("C# Queue trigger function processed: {messageText}", messageDecoding);
        MessageModel messageItem = JsonSerializer.Deserialize<MessageModel>(messageDecoding);
        var item = await _reviewPublisher.GetOneAsync(messageItem.Id);
        _logger.LogInformation("{test}",  item);
    }   
}