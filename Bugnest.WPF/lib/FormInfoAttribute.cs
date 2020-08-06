using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;

namespace Bugnest.WPF.lib
{
    public class FormInfoAttribute:Attribute
    {
        public string Label { get; set; }
        public Type ControlType { get; set; }
        public bool IsReadOnly { get; set; }

        public FormInfoAttribute(string label, Type controlType)
        {
            this.Label = label;
            this.ControlType = controlType;
        }
    }
}
