using Azure.Storage.Queues.Models;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using Migration.Services;
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.DependencyInjection;
using Migration.Documents;
using Migration.Models;
using Microsoft.Extensions.Options;

namespace Migration;

public class Syncronize
{
    private readonly ILogger<Syncronize> _logger;
    private readonly SqlServiceResolver _sqlServiceResolver;
    private readonly IServiceProvider _provider;
    private readonly IOptions<PublisherDatabaseSettings> _settings;
    private readonly string _functionName = "C# Queue trigger syncronize";

    public Syncronize(
        ILogger<Syncronize> logger, 
        SqlServiceResolver sqlServiceResolver,  
        IServiceProvider provider,
        IOptions<PublisherDatabaseSettings> settings
    )
    {
        _logger = logger;
        _sqlServiceResolver = sqlServiceResolver;
        _provider = provider;
        _settings = settings;
    }

    [Function(nameof(Syncronize))]
    public async Task Run([QueueTrigger("publisher", Connection = "AzureWebJobsStorage")] QueueMessage message)
    {
        var messageDecoding = Encoding.UTF8.GetString(Convert.FromBase64String(message.MessageText));
        _logger.LogInformation("{functionName} function processed: {messageText}", _functionName, messageDecoding);
        try
        {
            MessageModel? messageItem = JsonSerializer.Deserialize<MessageModel>(messageDecoding);
            //await _reviewPublisher.TestConnectionAsync();
            _logger.LogInformation("{functionName} - Getting sql services");
            var currentService = _sqlServiceResolver.Resolve(messageItem.TableName);
            var item = await currentService.GetOneAsync(messageItem.Id);
            PublisherImageService? imageService = _sqlServiceResolver.Resolve(_settings.Value.ImageTableName) as PublisherImageService;
            PublisherVideoService? videoService = _sqlServiceResolver.Resolve(_settings.Value.VideoTableName) as PublisherVideoService;

            if (item is ReviewModel reviewModel)
            {
                PublisherLenService? lenService = _sqlServiceResolver.Resolve(_settings.Value.LenTableName) as PublisherLenService;
                ReaderReviewService readerReviewService = _provider.GetRequiredService<ReaderReviewService>();
                _logger.LogInformation("{functionName} - Get one review: {reviewId} ", _functionName, reviewModel.Id);
                ReviewDocument? reviewDocument = await readerReviewService.GetAsync(reviewModel.Id.ToString());
                
                _logger.LogInformation(
                    "{functionName} - querying for image, video, len and cameras related",
                    _functionName
                );
                ImageModel? image = await imageService.GetOneAsync(reviewModel.ImageId) as ImageModel;
                VideoModel? video = await videoService.GetOneAsync(reviewModel.VideoId) as VideoModel;
                LenModel? len = await lenService.GetOneAsync(reviewModel.LenId) as LenModel;
                
                if (messageItem.Type.Equals("create") || reviewDocument is null)
                {
                    _logger.LogInformation("{functionName} - Creating review", _functionName);
                    
                    await readerReviewService.CreateAsync(
                        new ReviewDocument
                        {
                            Id = reviewModel.Id.ToString(),
                            Title = reviewModel.Title,
                            Subtitle = reviewModel.Subtitle,
                            Body = reviewModel.Body,
                            DateCreated = reviewModel.DateCreated,
                            DateUpdated = reviewModel.DateUpdated,
                            Video = videoService.CreateDocument(video),   
                            Image = imageService.CreateDocument(image),
                            Len =  await lenService.CreateDocument(len)
                        }
                    );
                }
                else
                {
                    _logger.LogInformation("{functionName} - Updating review", _functionName);

                    reviewDocument.Title = reviewModel.Title;
                    reviewDocument.Subtitle = reviewModel.Subtitle;
                    reviewDocument.Body = reviewModel.Body;
                    reviewDocument.DateUpdated = reviewModel.DateUpdated;
                    reviewDocument.Video = videoService.CreateDocument(video);
                    reviewDocument.Image = imageService.CreateDocument(image);
                    
                    await readerReviewService.UpdateAsync(
                        reviewDocument.Id,
                        reviewDocument
                    );
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogInformation("{functionName}failed {exception}", _functionName, ex);
        }
    }   
}