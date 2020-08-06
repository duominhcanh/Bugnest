using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace Bugnest.WPF.lib
{
    public class InputDialog:Window
    {
        public object CurrentObj { get; set; }

        public InputDialog(object obj)
        {
            this.CurrentObj = obj;
            Grid rootGrid = new Grid();

            var objProps = ((System.Reflection.TypeInfo)obj.GetType()).DeclaredProperties;
            rootGrid.ColumnDefinitions.Add(new ColumnDefinition() { Width = GridLength.Auto });
            rootGrid.ColumnDefinitions.Add(new ColumnDefinition() { Width = new GridLength(1, GridUnitType.Star) });
            for (int i = 0; i < objProps.Count(); i++)
            {
                var formInfo = (FormInfoAttribute)objProps.ElementAt(i).GetCustomAttributes(typeof(FormInfoAttribute), true).FirstOrDefault();

                var inpControl = (Control)Activator.CreateInstance(formInfo.ControlType);
                var inpLabel = new TextBlock();

                rootGrid.RowDefinitions.Add(new RowDefinition() { Height = GridLength.Auto });
                inpLabel.SetValue(Grid.RowProperty, i);
                inpLabel.SetValue(Grid.ColumnProperty, 0);
                inpControl.SetValue(Grid.RowProperty, i);
                inpControl.SetValue(Grid.ColumnProperty, 1);
                if(i > 0)
                {
                    inpLabel.Margin = new Thickness(0, 10, 0, 0);
                    inpControl.Margin = new Thickness(5, 10, 0, 0);
                }
                else
                {
                    inpControl.Margin = new Thickness(5, 0, 0, 0);
                }

                if (inpControl.GetType() == typeof(TextBox))
                {
                    Binding myBinding = new Binding();
                    myBinding.Source = CurrentObj;
                    myBinding.Path = new PropertyPath(objProps.ElementAt(i).Name);
                    myBinding.Mode = BindingMode.TwoWay;
                    myBinding.UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged;
                    BindingOperations.SetBinding(inpControl, TextBox.TextProperty, myBinding);

                    (inpControl as TextBox).IsReadOnly = formInfo.IsReadOnly;
                }
                else if (inpControl.GetType() == typeof(DatePicker))
                {
                    Binding myBinding = new Binding();
                    myBinding.Source = CurrentObj;
                    myBinding.Path = new PropertyPath(objProps.ElementAt(i).Name);
                    myBinding.Mode = BindingMode.TwoWay;
                    myBinding.UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged;
                    BindingOperations.SetBinding(inpControl, DatePicker.SelectedDateProperty, myBinding);
                }


                inpLabel.Text = formInfo.Label;

                rootGrid.Children.Add(inpLabel);
                rootGrid.Children.Add(inpControl);
            }
            rootGrid.RowDefinitions.Add(new RowDefinition() { Height = GridLength.Auto });
            StackPanel controlPanel = new StackPanel()
            {
                Orientation= Orientation.Horizontal,
                HorizontalAlignment= HorizontalAlignment.Right
            };

            Button saveButton = new Button() 
            {
                Content = "Lưu",
                Margin = new Thickness(0, 20, 0, 0),
                Width= 100
            };
            saveButton.Click += (sender, e) => { this.doSave(); };
            controlPanel.SetValue(Grid.RowProperty, objProps.Count());
            controlPanel.SetValue(Grid.ColumnSpanProperty, 2);
            controlPanel.Children.Add(saveButton);
            rootGrid.Children.Add(controlPanel);


            rootGrid.Margin = new Thickness(5);
            this.Content = rootGrid;
            this.Width = 400;
            this.SizeToContent = SizeToContent.Height;
            this.WindowStartupLocation = WindowStartupLocation.CenterScreen;
        }

        private void doSave()
        {
            this.Close();
        }

        public static T ShowInput<T>(T obj, Window owner= null)
        {
            InputDialog inputDialog = new InputDialog(obj) { Owner= owner };
            inputDialog.ShowDialog();
            return (T)inputDialog.CurrentObj;
        }
    }
}
