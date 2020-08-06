using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Bugnest.Site.Models
{
    public class Transaction
    {
        public Guid TransactionID { get; set; }
        public string CustomerName { get; set; }
        public int Ammount { get; set; }
    }
}