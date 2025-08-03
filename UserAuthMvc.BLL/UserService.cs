using System;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using UserAuthMvc.DAL;
using UserAuthMvc.Entities;

namespace UserAuthMvc.BLL
{
    public class UserService
    {
        private readonly ApplicationDbContext _context;
        public UserService(ApplicationDbContext context)
        {
            _context = context;
        }

        public User? Authenticate(string email, string password)
        {
            var user = _context.Users.FirstOrDefault(u => u.Email == email);
            if (user == null) return null;
            if (user.PasswordHash != HashPassword(password)) return null;
            return user;
        }

        public bool Register(string username, string email, string password, bool isAdmin = false)
        {
            if (_context.Users.Any(u => u.Email == email)) return false;
            var user = new User
            {
                UserName = username,
                Email = email,
                PasswordHash = HashPassword(password),
                IsAdmin = isAdmin
            };
            _context.Users.Add(user);
            _context.SaveChanges();
            return true;
        }

        public bool RequestPasswordReset(string email, out string token)
        {
            token = null;
            try
            {
                var user = _context.Users.FirstOrDefault(u => u.Email == email);
                if (user == null) return false;
                
                // Güvenli token oluştur
                token = Guid.NewGuid().ToString();
                user.ResetToken = token;
                user.ResetTokenExpiry = DateTime.Now.AddHours(1);
                _context.SaveChanges();
                return true;
            }
            catch (Exception)
            {
                token = null;
                return false;
            }
        }

        public bool ResetPassword(string token, string newPassword)
        {
            var user = _context.Users.FirstOrDefault(u => u.ResetToken == token && u.ResetTokenExpiry > DateTime.Now);
            if (user == null) return false;
            user.PasswordHash = HashPassword(newPassword);
            user.ResetToken = null;
            user.ResetTokenExpiry = null;
            _context.SaveChanges();
            return true;
        }

        public bool IsAdmin(string email)
        {
            var user = _context.Users.FirstOrDefault(u => u.Email == email);
            return user != null && user.IsAdmin;
        }

     

        private string HashPassword(string password)
        {
            using (var sha256 = SHA256.Create())
            {
                var bytes = Encoding.UTF8.GetBytes(password);
                var hash = sha256.ComputeHash(bytes);
                return Convert.ToBase64String(hash);
            }
        }
    }
}
