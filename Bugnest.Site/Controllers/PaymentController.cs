using Bugnest.Site.Models;
using Bugnest.Site.Models.FormData;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace Bugnest.Site.Controllers
{
    public class PaymentController : Controller
    {
        // GET: Payment
        public ActionResult Pay()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Pay(PayViewData viewData)
        {
            Transaction trans = new Transaction();

            trans.TransactionID = Guid.NewGuid();
            trans.CustomerName = viewData.CustomerName;
            trans.Ammount = viewData.Ammount;

            Session.Add("Transaction", viewData);

            return Redirect("PayMethod");
        }

        public ActionResult PayMethod()
        {
            return View();
        }
    }
}