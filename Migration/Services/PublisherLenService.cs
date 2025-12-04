using Migration.Models;
using Microsoft.Extensions.Options;
using Microsoft.Extensions.DependencyInjection;
using Migration.Documents;

namespace Migration.Services;

public class PublisherLenService (
    IOptions<PublisherDatabaseSettings> settings, 
    IServiceProvider provider
    ) : SqlService<LenModel>(settings, settings.Value.LenTableName)
{
    public async Task <Len?> CreateDocument(LenModel? len)
    {
        if (len is null) return null;
        
        PublisherImageService imageService = provider.GetRequiredService<PublisherImageService>();
        PublisherVideoService videoService = provider.GetRequiredService<PublisherVideoService>();
        
        ImageModel? image = await imageService.GetOneAsync(len.ImageId) as ImageModel;
        VideoModel? video = await videoService.GetOneAsync(len.VideoId) as VideoModel;
        
        return new Len
        {
            Id = len.Id.ToString(),
            ModelName = len.ModelName,
            VersionName = len.VersionName,
            MaxResolution = len.MaxResolution,
            SensorSize = len.SensorSize,
            EffectivePixels = len.EffectivePixels,
            Video = videoService.CreateDocument(video),
            Image = imageService.CreateDocument(image)
        };
    }
}