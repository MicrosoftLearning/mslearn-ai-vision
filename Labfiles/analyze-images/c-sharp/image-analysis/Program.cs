using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.Extensions.Configuration;
using Azure;
using SkiaSharp;

// Import namespaces


namespace image_analysis
{
    class Program
    {
        
        static async Task Main(string[] args)
        {
            // Clear the console
            Console.Clear();
            
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

      
                // Get image captions
                

                // Get image tags
                

                // Get objects in the image
                

                // Get people in the image
                

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task ShowObjects(string imageFile, ObjectsResult detectedObjects)
        {
            Console.WriteLine("\nAnnotating objects...");

            // Load the image using SkiaSharp
            using SKBitmap bitmap = SKBitmap.Decode(imageFile);
            using SKCanvas canvas = new SKCanvas(bitmap);

            // Set up styles for drawing
            SKPaint paint = new SKPaint
            {
                Color = SKColors.Cyan,
                StrokeWidth = 3,
                Style = SKPaintStyle.Stroke
            };

            SKPaint textPaint = new SKPaint
            {
                Color = SKColors.Cyan,
                IsAntialias = true
            };

            SKFont textFont = new SKFont(SKTypeface.Default,24,1,0);
            
            foreach (DetectedObject detectedObject in detectedObjects.Values)
            {
                // Draw object bounding box
                var r = detectedObject.BoundingBox;
                SKRect rect = new SKRect(r.X, r.Y, r.X + r.Width, r.Y + r.Height);
                canvas.DrawRect(rect, paint);
            }

            // Save the annotated image
            var objectFile = "objects.jpg";
            using SKFileWStream output = new SKFileWStream(objectFile);
            bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
            Console.WriteLine($"  Results saved in {objectFile}\n");
        }

        static async Task ShowPeople(string imageFile, PeopleResult detectedPeople)
        {
            Console.WriteLine("\nAnnotating people...");

            using SKBitmap bitmap = SKBitmap.Decode(imageFile);
            using SKCanvas canvas = new SKCanvas(bitmap);

            SKPaint paint = new SKPaint
            {
                Color = SKColors.Cyan,
                StrokeWidth = 3,
                Style = SKPaintStyle.Stroke
            };

            foreach (DetectedPerson person in detectedPeople.Values)
            {
                if (person.Confidence > 0.2)
                {
                    // Draw bounding box
                    var r = person.BoundingBox;
                    SKRect rect = new SKRect(r.X, r.Y, r.X + r.Width, r.Y + r.Height);
                    canvas.DrawRect(rect, paint);
                }
            }

            // Save the annotated image
            var peopleFile = "people.jpg";
            using SKFileWStream output = new SKFileWStream(peopleFile);
            bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
            Console.WriteLine($"  Results saved in {peopleFile}\n");
        }
    }
}
