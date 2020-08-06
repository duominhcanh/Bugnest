using Bugnest.Bingwall.Models;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Threading;

namespace Bugnest.Bingwall
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        [DllImport("user32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        static extern bool SystemParametersInfo(uint uiAction, uint uiParam, String pvParam, uint fWinIni);

        private const uint SPI_SETDESKWALLPAPER = 0x14;
        private const uint SPIF_UPDATEINIFILE = 0x1;
        private const uint SPIF_SENDWININICHANGE = 0x2;

        public List<BingApiResponseData> BingApiResponseDatas { get; set; }

        public MainWindow()
        {
            InitializeComponent();

            BtnGet.MouseUp += (sender, e) => { this.doLoadImages(); };
            BtnApply.MouseUp += (sender, e) => { this.doApplyDesktop(); };
            ListBox.SelectionChanged += (sender, e) =>
            {
                try
                {
                    BingApiResponseData bingApiResponseData = (BingApiResponseData)ListBox.SelectedItems[0];

                    RootGrid.Background = new ImageBrush { ImageSource = bingApiResponseData.Image };
                }
                catch
                {

                }
            };
            BtnClose.MouseUp += (sender, e) => { this.Close(); };
            RootCanvas.MouseDown += (sender, e) => { try { this.DragMove(); } catch { } };


            this.doLoadImages();
        }

        private void doApplyDesktop()
        {
            BingApiResponseData bingApiResponseData = (BingApiResponseData)ListBox.SelectedItems[0];

            string filePath = System.AppDomain.CurrentDomain.BaseDirectory + "desktop" + ".jpg";

            BitmapImage bitmapImage = bingApiResponseData.Image;
            if (bitmapImage.IsDownloading)
            {
                MessageBox.Show("Downloading");
            }
            else
            {
                BitmapEncoder encoder = new PngBitmapEncoder();
                encoder.Frames.Add(BitmapFrame.Create(bitmapImage));

                using (var fileStream = new System.IO.FileStream(filePath, System.IO.FileMode.Create))
                {
                    encoder.Save(fileStream);
                }

                set_Desktop_Background(filePath);
            }
        }

        private void doLoadImages()
        {
            BackgroundWorker backgroundWorker = new BackgroundWorker();
            backgroundWorker.DoWork += (sender, e) =>
            {
                BingApiResponseDatas = GetBingImages(8, "vi-VN");
            };
            backgroundWorker.RunWorkerCompleted += (sender, e) =>
            {
                Application.Current.Dispatcher.BeginInvoke(DispatcherPriority.Background,
                new Action(() =>
                {
                    ListBox.ItemsSource = BingApiResponseDatas;
                    ListBox.SelectedItem = BingApiResponseDatas[0];
                }));
            };
            backgroundWorker.RunWorkerAsync();
        }

        public List<BingApiResponseData> GetBingImages(int numOfImages, string region)
        {
            List<BingApiResponseData> listResponseData = new List<BingApiResponseData>();

            string strBingImageURL = string.Format("http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={0}&mkt={1}", numOfImages, region);

            HttpClient client = new HttpClient();
            client.BaseAddress = new Uri(strBingImageURL);

            client.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json"));
            HttpResponseMessage response = client.GetAsync("").Result;
            if (response.IsSuccessStatusCode)
            {
                var dataObjects = response.Content.ReadAsStringAsync().Result;
                for (int i = 0; i < numOfImages; i++)
                {
                    BingApiResponseData bingApiResponseData = new BingApiResponseData()
                    {
                        Title = Convert.ToString((JsonConvert.DeserializeObject<dynamic>(dataObjects)).images[i].title),
                        Url = Convert.ToString((JsonConvert.DeserializeObject<dynamic>(dataObjects)).images[i].url),
                        UrlBase = Convert.ToString((JsonConvert.DeserializeObject<dynamic>(dataObjects)).images[i].urlbase)
                    };
                    listResponseData.Add(bingApiResponseData);
                }
            }
            else
            {
                MessageBox.Show(string.Format("{0} ({1})", (int)response.StatusCode, response.ReasonPhrase));
            }
            client.Dispose();

            return listResponseData;
        }

        private void set_Desktop_Background(string sFile_FullPath)

        {

            //----------< btnSave_Click() >----------

            const int SET_DESKTOP_BACKGROUND = 20;

            const int UPDATE_INI_FILE = 1;

            const int SEND_WINDOWS_INI_CHANGE = 2;



            //--< set desktop.background >--

            win32.SystemParametersInfo(SET_DESKTOP_BACKGROUND, 0, sFile_FullPath, UPDATE_INI_FILE | SEND_WINDOWS_INI_CHANGE);

            //--</ set desktop.background >--

            //----------</ btnSave_Click() >----------

        }



        internal sealed class win32
        {
            [DllImport("user32.dll", CharSet = CharSet.Auto)]

            internal static extern int SystemParametersInfo(

                int uAction,

                int uParam,

                String lpvParam,

                int fuWinIni);

            //----</ .SystemParametersInfo() >----

            //----------</ win32 methods >----------

        }
    }
}
