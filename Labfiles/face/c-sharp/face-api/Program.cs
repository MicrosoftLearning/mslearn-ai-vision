using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Azure;
using SkiaSharp;

// Import namespaces



namespace analyze_faces
{
    class Program
    {

        static void Main(string[] args)
        {
            // Clear the console
            Console.Clear();
            
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string cogSvcEndpoint = configuration["AIServicesEndpoint"];
                string cogSvcKey = configuration["AIServiceKey"];

                // Get image
                string imageFile = "images/face1.jpg";
                if (args.Length > 0)
                {
                    imageFile = args[0];
                }

                // Authenticate Face client



                /// Specify facial features to be retrieved



                // Get faces
                
                

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static void AnnotateFaces(string imageFile, IReadOnlyList<FaceDetectionResult> detectedFaces)
        {
            Console.WriteLine($"\nAnnotating faces in image...");

            // Load the image using SkiaSharp
            using SKBitmap bitmap = SKBitmap.Decode(imageFile);
            using SKCanvas canvas = new SKCanvas(bitmap);

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

            // Annotate each face in the image
            int faceCount=0;
            foreach (var face in detectedFaces)
            {
                faceCount++;
                var r = face.FaceRectangle;
                SKRect rect = new SKRect(r.Left, r.Top, r.Left + r.Width, r.Top + r.Height);
                canvas.DrawRect(rect, rectPaint);

                string annotation = $"Face number {faceCount}";
                canvas.DrawText(annotation, r.Left, r.Top, SKTextAlign.Left, textFont, textPaint);
            }

            // Save annotated image
            var outputFile = "detected_faces.jpg";
            using (SKFileWStream output = new SKFileWStream(outputFile))
            {
                bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
            }

            Console.WriteLine($"  Results saved in {outputFile}\n"); 
        }
    }
}
