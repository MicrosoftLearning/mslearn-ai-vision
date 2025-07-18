using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Azure;
using SkiaSharp;

// Import namespaces



namespace read_text
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
                string aiSvcEndpoint = configuration["AIServicesEndpoint"];
                string aiSvcKey = configuration["AIServicesKey"];

                // Get image
                string imageFile = "images/Lincoln.jpg";
                if (args.Length > 0)
                {
                    imageFile = args[0];
                }
                
                // Authenticate Azure AI Vision client
                

                
                // Read text in image


                // Print the text
                        

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static void AnnotateLines(string imageFile, ReadResult detectedText)
        {
            Console.WriteLine($"\nAnnotating lines of text in image...");
            
            // Load the image using SkiaSharp
            using SKBitmap bitmap = SKBitmap.Decode(imageFile);
            // Create canvas to draw on the bitmap
            using SKCanvas canvas = new SKCanvas(bitmap);

            // Create paint for drawing polygons (bounding boxes)
            SKPaint paint = new SKPaint
            {
                Color = SKColors.Cyan,
                StrokeWidth = 3,
                Style = SKPaintStyle.Stroke,
                IsAntialias = true
            };

            foreach (var line in detectedText.Blocks.SelectMany(block => block.Lines))
            {
                var r = line.BoundingPolygon;
                SKPoint[] polygonPoints = new SKPoint[]
                {
                    new SKPoint(r[0].X, r[0].Y),
                    new SKPoint(r[1].X, r[1].Y),
                    new SKPoint(r[2].X, r[2].Y),
                    new SKPoint(r[3].X, r[3].Y)
                };
                // Call helper method to draw a polygon
                DrawPolygon(canvas, polygonPoints, paint);

            }

            // Save the annotated image using SkiaSharp
            var textFile = "lines.jpg";
            using (SKFileWStream output = new SKFileWStream(textFile))
            {
                // Encode the bitmap into JPEG format with full quality (100)
                bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
            }
            Console.WriteLine($"  Results saved in {textFile}\n");
        }

        static void AnnotateWords(string imageFile, ReadResult detectedText)
        {
            Console.WriteLine($"\nAnnotating individual words in image...");
            
            // Load the image using SkiaSharp
            using SKBitmap bitmap = SKBitmap.Decode(imageFile);
            // Create canvas to draw on the bitmap
            using SKCanvas canvas = new SKCanvas(bitmap);

            // Create paint for drawing polygons (bounding boxes)
            SKPaint paint = new SKPaint
            {
                Color = SKColors.Cyan,
                StrokeWidth = 3,
                Style = SKPaintStyle.Stroke,
                IsAntialias = true
            };

            foreach (var line in detectedText.Blocks.SelectMany(block => block.Lines))
            {
                // Find individual words in the line
                foreach (DetectedTextWord word in line.Words)
                {
                    // Convert the bounding polygon into an array of SKPoints
                    var r = word.BoundingPolygon;    
                    SKPoint[] polygonPoints = new SKPoint[]
                    {
                        new SKPoint(r[0].X, r[0].Y),
                        new SKPoint(r[1].X, r[1].Y),
                        new SKPoint(r[2].X, r[2].Y),
                        new SKPoint(r[3].X, r[3].Y)
                    };

                    // Draw the word polygon on the canvas
                    DrawPolygon(canvas, polygonPoints, paint);
                }
            }

            // Save the annotated image using SkiaSharp
            var textFile = "words.jpg";
            using (SKFileWStream output = new SKFileWStream(textFile))
            {
                // Encode the bitmap into JPEG format with full quality (100)
                bitmap.Encode(output, SKEncodedImageFormat.Jpeg, 100);
            }
            Console.WriteLine($"  Results saved in {textFile}\n");
        }

        // Helper method to draw a polygon given an array of SKPoints
        static void DrawPolygon(SKCanvas canvas, SKPoint[] points, SKPaint paint)
        {
            if (points == null || points.Length == 0)
                return;

            using (var path = new SKPath())
            {
                path.MoveTo(points[0]);
                for (int i = 1; i < points.Length; i++)
                {
                    path.LineTo(points[i]);
                }
                path.Close();
                canvas.DrawPath(path, paint);
            }
        }
    }
}

