using Microsoft.EntityFrameworkCore;
using UserAuthMvc.Entities;

namespace UserAuthMvc.DAL
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }

        public DbSet<User> Users { get; set; }
        public DbSet<PasswordReset> PasswordResets { get; set; }
    }
}
