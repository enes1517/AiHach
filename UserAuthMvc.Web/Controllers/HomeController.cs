using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using UserAuthMvc.Web.Models;

namespace UserAuthMvc.Web.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            var userEmail = HttpContext.Session.GetString("UserEmail");
            if (string.IsNullOrEmpty(userEmail))
            {
                return RedirectToAction("Login", "Account");
            }
            ViewBag.UserEmail = userEmail;
            return View();
        }

        public IActionResult Privacy()
        {
            return Content("Bu uygulama örnek bir kullanıcı yönetim sistemidir.");
        }

        
    }
}
