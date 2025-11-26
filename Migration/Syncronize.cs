using Azure.Storage.Queues.Models;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using Migration.Services;
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.DependencyInjection;
using Migration.Documents;
using Migration.Models;
using System;

namespace Migration;

public class Syncronize
{
    private readonly ILogger<Syncronize> _logger;
    private readonly SqlServiceResolver _sqlServiceResolver;
    private readonly IServiceProvider _provider;

    public Syncronize(ILogger<Syncronize> logger, SqlServiceResolver sqlServiceResolver,  IServiceProvider provider)
    {
        _logger = logger;
        _sqlServiceResolver = sqlServiceResolver;
        _provider = provider;
    }

    [Function(nameof(Syncronize))]
    public async Task Run([QueueTrigger("publisher", Connection = "AzureWebJobsStorage")] QueueMessage message)
    {
        var messageDecoding = Encoding.UTF8.GetString(Convert.FromBase64String(message.MessageText));
        _logger.LogInformation("C# Queue trigger function processed: {messageText}", messageDecoding);
        MessageModel? messageItem = JsonSerializer.Deserialize<MessageModel>(messageDecoding);
        
        //await _reviewPublisher.TestConnectionAsync();
        var serviceReview = _sqlServiceResolver.Resolve(messageItem.TableName);
        //var imageService = _sqlServiceResolver.Resolve("publisher_image");
        var item = await serviceReview.GetOneAsync(messageItem.Id);

        if (item is ReviewModel reviewModel)
        {   
            ReaderReviewService readerReviewService = _provider.GetRequiredService<ReaderReviewService>();
            _logger.LogInformation("C# Queue trigger - Get one review: {reviewId} ", reviewModel.Id);
            ReviewDocument? reviewDocument = await readerReviewService.GetAsync(reviewModel.Id.ToString());
            if (messageItem.Type.Equals("create") || reviewDocument is null)
            {
                _logger.LogInformation("C# Queue trigger - Creating review");

                /*ImageModel? image = reviewModel.ImageId is not null
                    ? await imageService.GetOneAsync(reviewModel.ImageId)
                    : null;*/
                
                await readerReviewService.CreateAsync(
                    new ReviewDocument
                    {
                        Id = reviewModel.Id.ToString(),
                        Title = reviewModel.Title,
                        Subtitle = reviewModel.Subtitle,
                        Body = reviewModel.Body,
                        DateCreated =  reviewModel.DateCreated,
                        DateUpdated =   reviewModel.DateUpdated,
                        Video = null,   
                        Image = null,
                        Len =  null,
                            
                    }
                );
            }
            else
            {
                _logger.LogInformation("C# Queue trigger - Updating review");
            }
        }
    }   
}