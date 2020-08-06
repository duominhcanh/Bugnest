using System;
using System.Windows.Media.Imaging;

namespace Bugnest.Bingwall.Models
{
    public class BingApiResponseData
    {
        public string Url { get; set; }
        public string UrlBase { get; set; }
        public string Title { get; set; }
        public string ImageUrl { get => "https://www.bing.com" + this.Url; }

        public BitmapImage Image { get => new BitmapImage(new Uri(ImageUrl)); }
    }
}
