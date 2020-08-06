using Bugnest.WPF.lib;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;

namespace Bugnest.WPF.Model
{
    public class Employee
    {
        [FormInfo("Mã", typeof(TextBox), IsReadOnly =true)]
        public string ID { get; set; }
        [FormInfo("Tên", typeof(TextBox))]
        public string Name { get; set; }
        [FormInfo("Ngày sinh", typeof(DatePicker))]
        public DateTime Birth { get; set; }
    }
}
