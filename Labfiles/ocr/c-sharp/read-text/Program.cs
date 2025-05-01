using System;
using System.IO;
using System.Linq;
using System.Drawing;
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

                // Authenticate Azure AI Vision client


                // Menu for text reading functions
                Console.WriteLine("\nChoose an image to read (or press any other key to quit):\n\n1: Lincoln.jpg)\n2: Business-card.jpg\n3: Note.jpg\n\n");
                Console.WriteLine("Enter a number:");
                string command = Console.ReadLine();
                string imageFile;

                switch (command)
                {
                    case "1":
                        imageFile = "images/Lincoln.jpg";
                        GetTextRead(imageFile, client);
                        break;
                    case "2":
                        imageFile = "images/Business-card.jpg";
                        GetTextRead(imageFile, client);
                        break;
                    case "3":
                        imageFile = "images/Note.jpg";
                        GetTextRead(imageFile, client);
                        break;
                    default:
                        break;
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static void GetTextRead(string imageFile, ImageAnalysisClient client)
        {
            Console.WriteLine($"\nReading text from {imageFile} \n");

            // Use a file stream to pass the image data to the analyze call
            using FileStream stream = new FileStream(imageFile,
                                                     FileMode.Open);

            // Use Analyze image function to read text in image
            
    
        }
    }
}

