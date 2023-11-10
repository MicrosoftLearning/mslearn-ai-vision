using System;
using System.Drawing;
using Microsoft.Extensions.Configuration;
using Azure;
using System.IO;

// Import namespaces


namespace image_analysis
{
    class Program
    {

        static void Main(string[] args)
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
                AnalyzeImage(imageFile, cvClient);

                // Remove the background or generate a foreground matte from the image
                BackgroundForeground(imageFile, cvClient);

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static void AnalyzeImage(string imageFile, VisionServiceOptions serviceOptions)
        {
            Console.WriteLine($"\nAnalyzing {imageFile} \n");

            var analysisOptions = new ImageAnalysisOptions()
            {
                // Specify features to be retrieved

            };

            // Get image analysis

        }
        static void BackgroundForeground(string imageFile, VisionServiceOptions serviceOptions)
        {
            // Remove the background from the image or generate a foreground matte

        }
    }
}
