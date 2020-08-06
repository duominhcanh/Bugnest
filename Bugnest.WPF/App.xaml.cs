using Bugnest.WPF.lib;
using Bugnest.WPF.Model;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Linq;
using System.ServiceModel;
using System.Threading.Tasks;
using System.Windows;

namespace Bugnest.WPF
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private static ServiceHost WCFHost { get; set; }

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            this.MainWindow = new MainWindow();
            this.MainWindow.Show();
        }

        public static int StartWCFServices()
        {
            try
            {
                WCFHost = new ServiceHost(typeof(MyService));
                WCFHost.Open();
                return 0;
            }
            catch (System.ServiceModel.AddressAccessDeniedException)
            {
                return -1;
            }
            catch (System.ServiceModel.AddressAlreadyInUseException)
            {
                return -2;
            }            
        }
    }
}
