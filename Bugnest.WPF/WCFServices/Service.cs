using Bugnest.WPF;
using System;
using System.Collections.Generic;
using System.ServiceModel;
using System.ServiceModel.Channels;
using System.ServiceModel.Configuration;
using System.ServiceModel.Description;
using System.ServiceModel.Dispatcher;
using System.ServiceModel.Web;
using System.Windows;

namespace Bugnest
{
    [ServiceContract(Namespace = "BugnestDomain")]
    public interface IService
    {
        [OperationContract]
        [WebInvoke(Method = "GET", ResponseFormat = WebMessageFormat.Json, BodyStyle = WebMessageBodyStyle.Wrapped)]
        string SayHello();
    }
    public class MyService : IService
    {
        public string SayHello()
        {
            App.Current.Dispatcher.Invoke(() =>
            {
                new MainWindow().Show();
            });

            return $"Hello, busy World,{DateTime.Now.ToShortTimeString()}";
        }
    }
}