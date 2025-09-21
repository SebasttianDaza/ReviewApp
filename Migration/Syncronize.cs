using System;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Migration
{
    public class Syncronize
    {
        private readonly ILogger _logger;

        public Syncronize(ILoggerFactory loggerFactory)
        {
            _logger = loggerFactory.CreateLogger<Syncronize>();
        }

        [Function("Syncronize")]
        public void Run([TimerTrigger("*/5 * * * *")] TimerInfo myTimer)
        {
            _logger.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");
            
            if (myTimer.ScheduleStatus is not null)
            {
                _logger.LogInformation($"Next timer schedule at: {myTimer.ScheduleStatus.Next}");
            }
        }
    }
}
