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

        // Declare variable for Azure AI Vision client

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
                GetTextRead(imageFile);

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static void GetTextRead(string imageFile)
        {
            Console.WriteLine($"\nReading text from {imageFile} \n");

            // Use a file stream to pass the image data to the analyze call
            using FileStream stream = new FileStream(imageFile,
                                                     FileMode.Open);

            // Use Analyze image function to read text in image
            
    
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

