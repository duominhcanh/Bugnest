using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
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

namespace Bugnest.Bugpaste
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            if (Clipboard.ContainsText())
            {

            }
            else if(Clipboard.ContainsImage())
            {

            }
            else if (Clipboard.ContainsAudio())
            {

            }
            else if (Clipboard.ContainsData())
            {

            }
            else if (Clipboard.ContainsFileDropList()) 
            { 

            }
            InitializeComponent();
        }
    }
}
