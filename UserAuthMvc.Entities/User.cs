using System;
using System.ComponentModel.DataAnnotations;

namespace UserAuthMvc.Entities
{
    public class User
    {
        [Key]
        public int Id { get; set; }
        
        [Required(ErrorMessage ="Username is required")]
        [StringLength(50, ErrorMessage = "The Username can be up to 50 characters.")]
        public string UserName { get; set; } = null!;
        
        [Required(ErrorMessage = "E-Mail is required.")]
        [EmailAddress(ErrorMessage = "Please enter a valid e-mail address.")]
        public string Email { get; set; } = null!;
       
        [Required(ErrorMessage = "Password is required")]
        [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
        public string PasswordHash { get; set; } = null!;
        public bool IsAdmin { get; set; } = false;
        
        [StringLength(128, ErrorMessage = "The reset token can be up to 128 characters.")]
        public string? ResetToken { get; set; }
        public DateTime? ResetTokenExpiry { get; set; }
    }
}
