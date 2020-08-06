using CefSharp;
using System;
using System.Collections.Generic;
using System.Linq;
using System.ServiceModel;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Bugnest.WPF
{
    /// <summary>
    /// Interaction logic for Window1.xaml
    /// </summary>
    public partial class Window1 : Window
    {
        public Window1()
        {
            InitializeComponent();
            Browser.LoadingStateChanged += OnLoadingStateChanged;
            Browser.JsDialogHandler = new JsHandler();
        }

        private void OnLoadingStateChanged(object sender, LoadingStateChangedEventArgs args)
        {
            if (!args.IsLoading)
            {
                App.Current.Dispatcher.Invoke(() =>
                {
                    StatusText.Text = "Loaded";
                });
            }
        }
    }

    public class JsHandler : IJsDialogHandler
    {
        public bool OnBeforeUnloadDialog(IWebBrowser chromiumWebBrowser, IBrowser browser, string messageText, bool isReload, IJsDialogCallback callback)
        {
            throw new NotImplementedException();
        }

        public void OnDialogClosed(IWebBrowser browserControl, IBrowser browser)
        {
            throw new NotImplementedException();
        }
        public bool OnJSAlert(IWebBrowser browser, string url, string message)
        {
            MessageBox.Show("Alert Detected. Url : " + url + " \n message : " + message);
            return false;
        }
        public bool OnJSBeforeUnload(IWebBrowser browserControl, IBrowser browser, string message, bool isReload, IJsDialogCallback callback)
        {
            throw new NotImplementedException();
        }
        public bool OnJSConfirm(IWebBrowser browser, string url, string message, out bool retval)
        {
            MessageBox.Show("Confirm Detected. Url : " + url + " \n message : " + message);
            retval = false;
            return false;
        }
        public bool OnJSDialog(IWebBrowser browserControl, IBrowser browser, string originUrl, CefJsDialogType dialogType, string messageText, string defaultPromptText, IJsDialogCallback callback, ref bool suppressMessage)
        {
            if(MessageBox.Show(messageText, originUrl, MessageBoxButton.YesNo) == MessageBoxResult.Yes)
            {
                return true;
            }

            // Fire OnDialogClosed
            return false;
        }
        public bool OnJSPrompt(IWebBrowser browser, string url, string message, string defaultValue, out bool retval, out string result)
        {
            MessageBox.Show("Prompt Detected. Url : " + url + " \n message : " + message);
            retval = false;
            result = "";
            return false;
        }
        public void OnResetDialogState(IWebBrowser browserControl, IBrowser browser)
        {
            throw new NotImplementedException();
        }
    }
}
