using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Bugnest.WPF
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            this.Loaded += SelfLoaded;
            BrowseButton.Click += BrowseButtonClick;
        }

        private void BrowseButtonClick(object sender, RoutedEventArgs e)
        {
            
        }

        private void SelfLoaded(object sender, RoutedEventArgs e)
        {
            new Thread(() =>
            {
                int statusCode= App.StartWCFServices();
                switch (statusCode)
                {
                    case 0:
                        this.addEventLog("Khởi động WCF Services thành công");
                        break;
                    case -1:
                        this.addErrorLog("Không có quyền Admin để khởi động WCF Services");
                        break;
                    case -2:
                        this.addErrorLog("Port khởi động WCF Services đã được sử dụng");
                        break;
                }
            }).Start();
        }

        private void addEventLog(string msg)
        {
            App.Current.Dispatcher.Invoke(() =>
            {
                EventBox.Items.Add($"<{DateTime.Now.ToString("dd/MM/yyyy HH:mm")}> {msg}");
            });
        }
        private void addErrorLog(string msg)
        {
            App.Current.Dispatcher.Invoke(() =>
            {
                EventBox.Items.Add($"<{DateTime.Now.ToString("dd/MM/yyyy HH:mm")}> {msg}");
            });
        }
    }
}
