using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Migration.Documents;
using Migration.Services;

var builder = FunctionsApplication.CreateBuilder(args);

builder.ConfigureFunctionsWebApplication();

builder.Services
    .AddApplicationInsightsTelemetryWorkerService()
    .ConfigureFunctionsApplicationInsights();

builder.Services.Configure<ReaderDatabaseSettings>(
    builder.Configuration.GetSection("ReaderDatabaseSettings")
);

builder.Services.AddSingleton<ReviewService>();

builder.Build().Run();
