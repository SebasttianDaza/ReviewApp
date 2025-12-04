using Migration.Models;
using Microsoft.Extensions.Options;
using Microsoft.Extensions.DependencyInjection;
using Migration.Documents;

namespace Migration.Services;

public class PublisherCameraService (
    IOptions<PublisherDatabaseSettings> settings,
    IServiceProvider provider
    ) : SqlService<CameraModel>(settings, settings.Value.CameraTableName)
{
    public async Task<Camera?> CreateDocument(CameraModel? camera)
    {
        if (camera is null) return null;
        
        PublisherImageService imageService = provider.GetRequiredService<PublisherImageService>();
        PublisherVideoService videoService = provider.GetRequiredService<PublisherVideoService>();
        
        ImageModel? image = await imageService.GetOneAsync(camera.ImageId) as ImageModel;
        VideoModel? video = await videoService.GetOneAsync(camera.VideoId) as VideoModel;

        return new Camera
        {
            Id = camera.Id.ToString(),
            ModelName = camera.ModelName,
            Version = camera.Version,
            MaxResolution = camera.MaxResolution,
            SensorSize = camera.SensorSize,
            EffectivePixels = camera.EffectivePixels,
            StorageTypes = camera.StorageTypes,
            ScreenSize = camera.ScreenSize,
            Video = videoService.CreateDocument(video),
            Image = imageService.CreateDocument(image)
        };
    }
}