using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Migration.Documents;
using Migration.Models;
using Migration.Services;

var builder = FunctionsApplication.CreateBuilder(args);

builder.ConfigureFunctionsWebApplication();

builder.Services
    .AddApplicationInsightsTelemetryWorkerService()
    .ConfigureFunctionsApplicationInsights();

builder.Services.Configure<ReaderDatabaseSettings>(
    builder.Configuration.GetSection("ReaderDatabaseSettings")
);
builder.Services.Configure<PublisherDatabaseSettings>(
    builder.Configuration.GetSection("PublisherDatabaseSettings")
);

builder.Services.AddSingleton<PublisherReviewService>();
builder.Services.AddSingleton<ReviewReaderService>();

builder.Build().Run();
