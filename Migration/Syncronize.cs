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
    private readonly PublisherReviewService _publisherReview;

    public Syncronize(ILogger<Syncronize> logger, ReviewReaderService reviewReaderService, PublisherReviewService publisherReviewService)
    {
        _logger = logger;
        _publisherReview = publisherReviewService;
    }

    [Function(nameof(Syncronize))]
    public async Task Run([QueueTrigger("publisher", Connection = "AzureWebJobsStorage")] QueueMessage message)
    {
        var messageDecoding = Encoding.UTF8.GetString(Convert.FromBase64String(message.MessageText));
        _logger.LogInformation("C# Queue trigger function processed: {messageText}", messageDecoding);
        MessageModel messageItem = JsonSerializer.Deserialize<MessageModel>(messageDecoding);
        
        //await _reviewPublisher.TestConnectionAsync();
        
        var item = await _publisherReview.GetOneAsync(messageItem.Id);
        _logger.LogInformation("{test}", item.Title);
    }   
}