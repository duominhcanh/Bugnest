using Bugnest.WPF.lib;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;

namespace Bugnest.WPF.Model
{
    public class Bus
    {
        [FormInfo("Số Xe", typeof(TextBox))]
        public string Number { get; set; }
        [FormInfo("Chủ sở hữu", typeof(TextBox))]
        public string Owner { get; set; }
    }
}
