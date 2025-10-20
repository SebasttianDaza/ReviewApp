using System;
using Azure.Storage.Queues.Models;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Migration;

public class Syncronize
{
    private readonly ILogger<Syncronize> _logger;

    public Syncronize(ILogger<Syncronize> logger)
    {
        _logger = logger;
    }

    [Function(nameof(Syncronize))]
    public void Run([QueueTrigger("publisher", Connection = "")] QueueMessage message)
    {
        _logger.LogInformation("C# Queue trigger function processed: {messageText}", message.MessageText);
    }
}