using System;
using System.Threading.Tasks;
using System.Web;
using Microsoft.Owin;
using Owin;

[assembly: OwinStartup(typeof(Bugnest.Site.Startup))]

namespace Bugnest.Site
{
    public class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            
        }
    }
}
