using Migration.Models;
using Microsoft.Extensions.Options;
using Migration.Documents;

namespace Migration.Services;

public class PublisherVideoService(IOptions<PublisherDatabaseSettings> settings)
    : SqlService<VideoModel>(settings, settings.Value.VideoTableName)
{
    public Video? CreateDocument(VideoModel? video)
    {
        if (video is null) return null;

        return new Video
        {
            Title = video.Title,
            Description = video.Description,
            SourceId =  video.SourceId,
            Source = video.Source
        };
    }
}