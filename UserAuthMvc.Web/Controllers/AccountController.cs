using Microsoft.AspNetCore.Mvc;
using UserAuthMvc.BLL;
using UserAuthMvc.DAL;
using UserAuthMvc.Web.Models;

namespace UserAuthMvc.Web.Controllers
{
    public class AccountController : Controller
    {
        private readonly UserService _userService;
        public AccountController(ApplicationDbContext context)
        {
            _userService = new UserService(context);
        }

        [HttpGet]
        public IActionResult Register() => View();

        [HttpPost]
        public IActionResult Register(RegisterViewModel model)
        {
            if (!ModelState.IsValid)
            {
                ModelState.AddModelError(string.Empty, "Lütfen tüm alanları doğru doldurun.");
                return View(model);
            }
            if (model.Password != model.ConfirmPassword)
            {
                ModelState.AddModelError("Password", "Şifreler eşleşmiyor.");
                return View(model);
            }
            var result = _userService.Register(model.UserName, model.Email, model.Password);
            if (!result)
            {
                ModelState.AddModelError("Email", "Bu email zaten kayıtlı.");
                return View(model);
            }
            TempData["RegisterSuccess"] = "Kayıt başarılı! Şimdi giriş yapabilirsiniz.";
            return RedirectToAction("Login");
        }

        [HttpGet]
        public IActionResult Login() => View();

        [HttpPost]
        public IActionResult Login(LoginViewModel model)
        {
            if (!ModelState.IsValid)
            {
                ModelState.AddModelError(string.Empty, "Lütfen tüm alanları doğru doldurun.");
                return View(model);
            }
            var user = _userService.Authenticate(model.Email, model.Password);
            if (user == null)
            {
                ModelState.AddModelError("Email", "Geçersiz email veya şifre.");
                return View(model);
            }
            HttpContext.Session.SetString("UserEmail", user.Email);
            HttpContext.Session.SetString("IsAdmin", user.IsAdmin.ToString());
            return RedirectToAction("Index", "Home");
        }

        public IActionResult Logout()
        {
            HttpContext.Session.Clear();
            return RedirectToAction("Login");
        }

        [HttpGet]
        public IActionResult ResetPasswordRequest() => View();

        [HttpPost]
        public IActionResult ResetPasswordRequest(ResetPasswordRequestViewModel model)
        {
            if (!ModelState.IsValid)
            {
                ModelState.AddModelError(string.Empty, "Lütfen geçerli bir email girin.");
                return View(model);
            }
            if (_userService.RequestPasswordReset(model.Email, out var token))
            {
                ViewBag.Token = token;
                return View("ShowResetToken");
            }
            ModelState.AddModelError("Email", "Email bulunamadı.");
            return View(model);
        }

        [HttpGet]
        public IActionResult ResetPassword(string token)
        {
            return View(new ResetPasswordViewModel { Token = token });
        }

        [HttpPost]
        public IActionResult ResetPassword(ResetPasswordViewModel model)
        {
            if (!ModelState.IsValid)
            {
                ModelState.AddModelError(string.Empty, "Lütfen tüm alanları doğru doldurun.");
                return View(model);
            }
            if (model.NewPassword != model.ConfirmPassword)
            {
                ModelState.AddModelError("NewPassword", "Şifreler eşleşmiyor.");
                return View(model);
            }
            if (_userService.ResetPassword(model.Token, model.NewPassword))
            {
                TempData["ResetSuccess"] = "Şifre başarıyla değiştirildi. Giriş yapabilirsiniz.";
                return RedirectToAction("Login");
            }
            ModelState.AddModelError("Token", "Token geçersiz veya süresi dolmuş.");
            return View(model);
        }

        public IActionResult AdminPanel()
        {
            var isAdmin = HttpContext.Session.GetString("IsAdmin");
            if (isAdmin != "True") return Unauthorized();
            // Basit admin paneli: tüm kullanıcıları listele
            var users = _userService.GetAllUsers();
            return View(users);
        }

        [HttpGet]
        public IActionResult CreateTestUser()
        {
            // Sadece test için: Kullanıcıyı ekle
            var result = _userService.Register("enes", "enes@gmail.com", "2266");
            if (result)
                return Content("Test kullanıcısı oluşturuldu.");
            else
                return Content("Kullanıcı zaten mevcut.");
        }
    }
} 