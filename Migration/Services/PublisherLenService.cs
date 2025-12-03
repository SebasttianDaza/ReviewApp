using Migration.Models;
using Microsoft.Extensions.Options;
using Microsoft.Extensions.DependencyInjection;
using Migration.Documents;

namespace Migration.Services;

public class PublisherLenService (IOptions<PublisherDatabaseSettings> settings, SqlServiceResolver sqlServiceResolver)
    : SqlService<LenModel>(settings, settings.Value.LenTableName)
{
    public async Task <LenDocument?> CreateDocument(LenModel? len)
    {
        if (len is null) return null;
        
        PublisherImageService? imageService = sqlServiceResolver.Resolve(settings.Value.ImageTableName) as PublisherImageService;
        PublisherVideoService? videoService = sqlServiceResolver.Resolve(settings.Value.VideoTableName) as PublisherVideoService;
        
        ImageModel? image = await imageService.GetOneAsync(len.ImageId) as ImageModel;
        VideoModel? video = await videoService.GetOneAsync(len.VideoId) as VideoModel;
        
        return new LenDocument
        {
            Id = len.Id.ToString(),
            ModelName = len.ModelName,
            VersionName = len.VersionName,
            Description = len.Description,
            MaxResolution = len.MaxResolution,
            SensorSize = len.SensorSize,
            EffectivePixels = len.EffectivePixels,
            DateCreated = len.DateCreated,
            DateUpdated = len.DateUpdated,
            Video = videoService.CreateDocument(video),
            Image = imageService.CreateDocument(image),
        };
    }
}