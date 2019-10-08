﻿using Azure.Storage.Blobs.PerfStress.Core;
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

namespace Azure.Storage.Blobs.PerfStress
{
    public class GetBlobsTest : ContainerTest<CountOptions>
    {
        public GetBlobsTest(CountOptions options) : base(options)
        {
        }

        public override async Task GlobalSetup()
        {
            await base.GlobalSetup();

            var uploadTasks = new Task[Options.Count];
            for (var i = 0; i < uploadTasks.Length; i++)
            {
                var blobName = "getblobstest-" + Guid.NewGuid().ToString();
                uploadTasks[i] = BlobContainerClient.UploadBlobAsync(blobName, Stream.Null);
            }
            await Task.WhenAll(uploadTasks);
        }

        public override void Run(CancellationToken cancellationToken)
        {
            // Must enumerate collection to ensure all BlobItems are downloaded
            foreach (var _ in BlobContainerClient.GetBlobs(cancellationToken: cancellationToken));
        }

        public override async Task RunAsync(CancellationToken cancellationToken)
        {
            // Must enumerate collection to ensure all BlobItems are downloaded
            await foreach (var _ in BlobContainerClient.GetBlobsAsync(cancellationToken: cancellationToken)) { }
        }
    }
}
