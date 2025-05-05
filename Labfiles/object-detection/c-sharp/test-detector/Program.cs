using System;
using System.IO;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;
using SkiaSharp;
using Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction;
using Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction.Models;

namespace test_detector
{
    class Program
    {

        static CustomVisionPredictionClient prediction_client;

        static void Main(string[] args)
        {

            try
            {
                // Clear the console
                Console.Clear();

                // Get Configuration Settings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string prediction_endpoint = configuration["PredictionEndpoint"];
                string prediction_key = configuration["PredictionKey"];
                Guid project_id = Guid.Parse(configuration["ProjectID"]);
                string model_name = configuration["ModelName"];

                // Authenticate a client for the prediction API
                prediction_client = new CustomVisionPredictionClient(new Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction.ApiKeyServiceClientCredentials(prediction_key))
                {
                    Endpoint = prediction_endpoint
                };

                // Detect objects in the image
                String image_file = "produce.jpg";
                Console.WriteLine("Detecting objects in " + image_file);
                MemoryStream image_data = new MemoryStream(File.ReadAllBytes(image_file));
                var result = prediction_client.DetectImage(project_id, model_name, image_data);

                // Loop over each prediction
                foreach (var prediction in result.Predictions)
                {
                    // Get each prediction with a probability > 50%
                    if (prediction.Probability > 0.5)
                    {
                        Console.WriteLine($"{prediction.TagName}");
            
                    }
                }

                // Create and save an annotated image
                SaveTaggedImage(image_file, result.Predictions);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }

        }

        static void SaveTaggedImage(string sourcePath, IList<PredictionModel> detectedObjects)
        {
            // Load the image using SkiaSharp
            using SKBitmap bitmap = SKBitmap.Decode(sourcePath);
            int w = bitmap.Width;
            int h = bitmap.Height;
            using SKCanvas canvas = new SKCanvas(bitmap);

            // Set up paint styles for drawing
            SKPaint rectPaint = new SKPaint
            {
                Color = SKColors.LightGreen,
                StrokeWidth = 3,
                Style = SKPaintStyle.Stroke,
                IsAntialias = true
            };

            SKPaint textPaint = new SKPaint
            {
                Color = SKColors.White,
                IsAntialias = true
            };

            SKFont textFont = new SKFont(SKTypeface.Default,24,1,0);

            // Loop over each prediction
            foreach (var detectedObject in detectedObjects)
            {
                // Show each prediction with a probability > 50%
                if (detectedObject.Probability > 0.5)
                {
                    // The bounding box sizes are proportional - convert to absolute
                    int left = Convert.ToInt32(detectedObject.BoundingBox.Left * w);
                    int top = Convert.ToInt32(detectedObject.BoundingBox.Top * h);
                    int height = Convert.ToInt32(detectedObject.BoundingBox.Height * h);
                    int width =  Convert.ToInt32(detectedObject.BoundingBox.Width * w);
                    SKRect rect = new SKRect(left, top, left + width, top + height);
                    canvas.DrawRect(rect, rectPaint);
                    string annotation = $"{detectedObject.TagName} ({detectedObject.Probability.ToString("P2")})";
                    canvas.DrawText(annotation, left, top, SKTextAlign.Left, textFont, textPaint);
        
                }
            }

            // Save annotated image
            var outputFile = "output.jpg";
            using (SKFileWStream output = new SKFileWStream(outputFile))
            {
                bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
            }
            Console.WriteLine($"Results saved in {outputFile}\n"); 
        }
    }
}
