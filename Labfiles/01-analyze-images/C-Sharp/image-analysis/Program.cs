using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Drawing;
using Microsoft.Extensions.Configuration;
using Azure;

// Import namespaces

namespace image_analysis
{
    class Program
    {

        static async Task Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string aiSvcEndpoint = configuration["AIServicesEndpoint"];
                string aiSvcKey = configuration["AIServicesKey"];

                // Get image
                string imageFile = "images/street.jpg";
                if (args.Length > 0)
                {
                    imageFile = args[0];
                }

                // Authenticate Azure AI Vision client

                
                // Analyze image
                AnalyzeImage(imageFile, client);

                // Remove the background or generate a foreground matte from the image
                await BackgroundForeground(imageFile, aiSvcEndpoint, aiSvcKey);

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static void AnalyzeImage(string imageFile, ImageAnalysisClient client)
        {
            Console.WriteLine($"\nAnalyzing {imageFile} \n");

            // Use a file stream to pass the image data to the analyze call
            using FileStream stream = new FileStream(imageFile,
                                                     FileMode.Open);

            // Get result with specified features to be retrieved
            
            
            // Display analysis results
            

        }
        static async Task BackgroundForeground(string imageFile, string endpoint, string key)
        {
            // Remove the background from the image or generate a foreground matte
            
        }
    }
}
